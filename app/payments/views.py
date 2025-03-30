# views.py
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from .models import PaymentAttempt, Payment, PaymentApplication, PaymentProvider, PaymentAttemptDebt
from parking.models import ParkingSessionModel
from decimal import Decimal
from django.db import transaction
from datetime import datetime


class KASSA24PaymentView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def get(self, request):
        action = request.query_params.get('action')
        license_plate = request.query_params.get('number')
        amount = request.query_params.get('amount', None)
        receipt = request.query_params.get('receipt', None)
        date = request.query_params.get('date', None)

        if action == 'check':
            # Handle check action
            debts = ParkingSessionModel.objects.filter(
                license_plate=license_plate,
                is_paid=False
            )

            total_due = sum([debt.calculate_due_amount() for debt in debts])

            if not debts or not total_due:
                return Response({
                    "Code": "2",
                    "Message": "Абонент не найден"
                }, status=status.HTTP_404_NOT_FOUND)

            # Create PaymentAttempt
            payment_attempt = PaymentAttempt.objects.create(
                license_plate=license_plate,
                amount=total_due,
                provider=PaymentProvider.KASSA24
            )

            for debt in debts:
                PaymentAttemptDebt.objects.create(
                    payment_attempt=payment_attempt,
                    content_type=ContentType.objects.get_for_model(debt),
                    object_id=debt.id
                )

            return Response({
                "Code": "0",
                "Message": "Абонент существует",
                "Date": timezone.now().strftime("%Y-%m-%dT%H:%M:%S"),
                "Invoice": [{
                   "amount": total_due
                }]
            }, status=status.HTTP_200_OK)

        elif action == 'payment':
            # Handle payment action
            if not receipt or not amount or not license_plate:
                return Response({
                    "Code": "1",
                    "Message": "Неверные параметры запроса"
                }, status=status.HTTP_400_BAD_REQUEST)

            # Validate the receipt (ensure payment is not duplicated)
            existing_payment = Payment.objects.filter(receipt=receipt).first()
            if existing_payment:
                return Response({
                    "Code": "0",
                    "Message": "Платёж уже был принят",
                    "AuthCode": existing_payment.id,
                    "Date": existing_payment.date.strftime("%Y-%m-%dT%H:%M:%S")
                }, status=status.HTTP_200_OK)

            # Find corresponding payment attempt
            payment_attempt = PaymentAttempt.objects.filter(
                license_plate=license_plate,
                status=PaymentAttempt.Status.PENDING,
                provider=PaymentProvider.KASSA24
            ).first()

            if not payment_attempt:
                return Response({
                    "Code": "2",
                    "Message": "Абонент не найден"
                }, status=status.HTTP_404_NOT_FOUND)

            date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")
            date = timezone.make_aware(date)

            # Create payment record
            payment = Payment.objects.create(
                license_plate=license_plate,
                receipt=receipt,
                amount=amount,
                date=date,
                provider=PaymentProvider.KASSA24,
                attempt=payment_attempt
            )

            # Apply payment to debts
            remaining_amount = Decimal(amount)
            for debt in payment_attempt.debts.all():
                if remaining_amount <= 0:
                    break
                debt_due = debt.debt_object.calculate_due_amount()
                to_apply = min(remaining_amount, debt_due)

                PaymentApplication.objects.create(
                    payment=payment,
                    debt_object=debt.debt_object,
                    amount_applied=to_apply
                )

                remaining_amount -= to_apply
                debt.debt_object.update_amount()

            # Mark payment attempt as paid
            payment_attempt.status = PaymentAttempt.Status.PAID
            payment_attempt.save()

            return Response({
                "Code": "0",
                "Message": "Платёж принят",
                "AuthCode": payment.id,
                "Date": payment.date.strftime("%Y-%m-%dT%H:%M:%S")
            }, status=status.HTTP_200_OK)

        else:
            return Response({
                "Code": "1",
                "Message": "Неизвестный тип запроса"
            }, status=status.HTTP_400_BAD_REQUEST)
