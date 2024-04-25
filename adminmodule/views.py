import razorpay
from django.http import  HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .forms import HotelPaymentForm
import razorpay
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import HotelPayment

from django.shortcuts import render, redirect
from .models import HotelPayment,Hotel,HotelImage
def add_hotel(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        location = request.POST.get('location')
        rating = request.POST.get('rating')
        room_type = request.POST.get('room_type')
        price_per_night = request.POST.get('price_per_night')
        number_of_rooms = request.POST.get('number_of_rooms')
        wifi_available = request.POST.get('wifi_available', False) == 'true'  # Convert to boolean
        pool_available = request.POST.get('pool_available', False) == 'true'  # Convert to boolean
        gym_available = request.POST.get('gym_available', False) == 'true'  # Convert to boolean
        Laundry_facilities = request.POST.get('Laundry_facilities', False) == 'true'
        Parking = request.POST.get('Parking', False) == 'true'
        Restaurant = request.POST.get('Restaurant', False) == 'true'
        images = request.FILES.getlist('images')

        # Create a new Hotel object with the provided data
        hotel = Hotel.objects.create(
            name=name,
            location=location,
            rating=rating,
            room_type=room_type,
            price_per_night=price_per_night,
            number_of_rooms=number_of_rooms,
            wifi_available=wifi_available,
            pool_available=pool_available,
            gym_available=gym_available,
        )
        # Set additional facilities if they are provided
        if hasattr(hotel, 'Laundry_facilities'):
            hotel.Laundry_facilities = Laundry_facilities
        if hasattr(hotel, 'Parking'):
            hotel.Parking = Parking
        if hasattr(hotel, 'Restaurant'):
            hotel.Restaurant = Restaurant

        for image in images:
            HotelImage.objects.create(hotel=hotel, image=image)

        hotel.save()
        return redirect('view_hotels')  # Redirect to view_hotels view
    return render(request, 'add_hotel.html')  # Render add_hotel.html template if request method is not POST

def view_hotels(request):
    hotels = Hotel.objects.all()
    return render(request, 'view_hotels.html', {'hotels': hotels})

def delete_hotel(request, pk):
    hotel = Hotel.objects.get(pk=pk)
    hotel.delete()
    return redirect(view_hotels)

def search_view(request):
    if request.method == 'GET':
        location = request.GET.get('location')
        results = Hotel.objects.filter(location__icontains=location)
        return render(request,'bookhotel.html',{'hotels': results})
    else:
        return render(request,{'error': 'Method not allowed'}, status=405)

def adminhomepage(request):
    return render(request,'adminhomepage.html')

def edit_hotel(request, pk):
    hotel = Hotel.objects.get(pk=pk)
    if request.method == 'POST':
        hotel.name = request.POST['name']
        hotel.location = request.POST['location']
        hotel.price_per_night = request.POST['price_per_night']
        hotel.rating = request.POST['rating']
        hotel.number_of_rooms = request.POST['number_of_rooms']
        hotel.room_type = request.POST['room_type']
        hotel.wifi_available = request.POST.get('wifi_available', False) == 'on'
        hotel.Laundry_facilities = request.POST.get('Laundry_Facilities', False) == 'on'
        hotel.pool_available = request.POST.get('pool_available', False) == 'on'
        hotel.Parking = request.POST.get('Parking', False) == 'on'
        hotel.gym_available = request.POST.get('gym_available', False) == 'on'
        hotel.Restaurant = request.POST.get('Restaurant', False) == 'on'
        hotel.save()
        return redirect("view_hotels")
    return render(request, 'edit_hotel.html', {'hotel': hotel})

def hoteloverview(request,hotel_id):
    hotel = Hotel.objects.filter(pk=hotel_id)
    return render(request,'hoteloverview.html',{'hotels': hotel})

def hotelpaymentmodule(request):
    response_payment = None
    if request.method == "POST":
        name = request.POST.get('name')
        amount = int(request.POST.get('amount', 0)) * 100

        # Creating Razorpay client
        client = razorpay.Client(auth=("rzp_test_e3EA7eBqB0PT2x", "mFr4KLidHO6bJEUOs71qX4jY"))

        # Create order
        response_payment = client.order.create({
            'amount': amount,
            'currency': 'INR'
        })
        order_id = response_payment['id']
        order_status = response_payment['status']
        if order_status == "created":
            hotel = HotelPayment(name=name, amount=amount, order_id=order_id)
            hotel.save()
            response_payment['name'] = name
            form = HotelPaymentForm(request.POST or None)
            return render(request, "hotel_payment.html", {'form': form, 'payment': response_payment})

    form = HotelPaymentForm()
    return render(request, 'hotel_payment.html', {'form': form, 'payment': response_payment})


@csrf_exempt
def paymentstatus(request):
    response = request.POST
    parms_dict = {
    "razorpay_payment_id":response["razorpay_payment_id"],
    "razorpay_order_id": response["razorpay_order_id"],
    "razorpay_signature": response["razorpay_signature"]
    }
    client = razorpay.Client(auth=("rzp_test_e3EA7eBqB0PT2x", "mFr4KLidHO6bJEUOs71qX4jY"))

    try:
        status = client.utility.verify_payment_signature(parms_dict)
        hotel = HotelPayment.objects.get(order_id=response['razorpay_order_id'])
        hotel.razorpay_payment_id = response['razorpay_payment_id']
        hotel.paid = True
        hotel.save()
        return render(request, 'payment-status.html', {'status': True})
    except:
        return render(request, 'payment-status.html', {'status': False})

