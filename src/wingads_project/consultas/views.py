from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required # Importar el decorador
from .forms import ConsultaForm, CustomUserCreationForm # Importar el formulario que acabamos de crear
from .models import Consulta, Pago # Importar el modelo Consulta y Pago
from django.conf import settings # Para acceder a las claves de Mercado Pago
import mercadopago # Importar la librería de Mercado Pago

# Create your views here.

def home(request):
    return render(request, 'consultas/index.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('consultas:home') # Redirige a la página de inicio después del registro
    else:
        form = CustomUserCreationForm()
    return render(request, 'consultas/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('consultas:home') # Redirige a la página de inicio después del login
    else:
        form = AuthenticationForm()
    return render(request, 'consultas/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('consultas:home') # Redirige a la página de inicio después del logout

@login_required
def crear_consulta(request):
    if request.method == 'POST':
        form = ConsultaForm(request.POST)
        if form.is_valid():
            consulta = form.save(commit=False)
            consulta.user = request.user # Asigna el usuario actual a la consulta
            # Aquí se podría calcular el precio basado en el tipo de consulta, por ahora lo asignamos.
            # Es importante manejar esto cuidadosamente para la integración de pagos.
            if consulta.tipo == 'basica':
                consulta.precio = 5000
            elif consulta.tipo == 'analisis':
                consulta.precio = 15000
            elif consulta.tipo == 'llamada':
                consulta.precio = 30000
            consulta.save()
            # Redirigir a la vista de inicio de pago
            return redirect('consultas:iniciar_pago', consulta_id=consulta.id)
    else:
        form = ConsultaForm()
    return render(request, 'consultas/crear_consulta.html', {'form': form})

@login_required
def iniciar_pago(request, consulta_id):
    try:
        consulta = Consulta.objects.get(id=consulta_id, user=request.user)
    except Consulta.DoesNotExist:
        return redirect('consultas:home') # O a una página de error

    # Crear un registro de Pago si no existe
    pago, created = Pago.objects.get_or_create(
        consulta=consulta,
        defaults={'monto': consulta.precio, 'estado_pago': 'pendiente'}
    )

    # Configurar el SDK de Mercado Pago
    sdk = mercadopago.SDK(settings.MERCADOPAGO_ACCESS_TOKEN)

    # Crear la preferencia de pago
    preference_data = {
        "items": [
            {
                "title": f"Consulta de {consulta.get_tipo_display()}",
                "quantity": 1,
                "unit_price": float(consulta.precio), # Convertir a float
            }
        ],
        "payer": {
            "email": request.user.email, # Usar el email del usuario registrado
        },
        "back_urls": {
            "success": request.build_absolute_uri('/pago_exitoso/'),
            "pending": request.build_absolute_uri('/pago_pendiente/'),
            "failure": request.build_absolute_uri('/pago_fallido/'),
        },
        "auto_return": "approved", # Redirige automáticamente al usuario después del pago exitoso
        "external_reference": str(pago.id), # Referencia interna para seguimiento
    }

    try:
        preference_response = sdk.preference().create(preference_data)
        print(f"Respuesta completa de Mercado Pago: {preference_response}")
        preference = preference_response["response"]
        print(f"Objeto preference extraído: {preference}")
        return redirect(preference["init_point"]) # Redirigir al usuario a la URL de pago de Mercado Pago
    except Exception as e:
        # Manejar el error de Mercado Pago
        print(f"Error al crear preferencia de pago: {e}")
        return render(request, 'consultas/error_pago.html', {'error': 'Error al iniciar el pago. Intente de nuevo más tarde.'})

@login_required
def pago_exitoso(request):
    # Aquí puedes procesar la confirmación del pago, verificar la transacción, etc.
    # Por ahora, solo muestra una página de éxito.
    return render(request, 'consultas/pago_exitoso.html')

@login_required
def pago_pendiente(request):
    # Aquí puedes procesar el estado pendiente del pago
    return render(request, 'consultas/pago_pendiente.html')

@login_required
def pago_fallido(request):
    # Aquí puedes manejar pagos fallidos
    return render(request, 'consultas/pago_fallido.html')
