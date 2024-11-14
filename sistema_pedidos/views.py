from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from .models import Mesa, Producto, Pedido, DetallePedido
from django.shortcuts import render
from .models import Mesa, Producto
from django.shortcuts import render
from .models import Producto
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Mesa
from django.urls import reverse
from django.http import JsonResponse
from .models import Pedido



def admin_home(request):
    """Vista principal del administrador."""
    return render(request, 'admin_home.html')


def index(request):
    """Vista principal donde las mesas pueden ver el menú."""
    if not request.user.is_authenticated or not hasattr(request.user, 'mesa'):
        return redirect('login')

    productos = Producto.objects.all()
    return render(request, 'index.html', {'productos': productos})


def login_user(request):
    """Inicia sesión para una mesa."""
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        
        if user is not None and hasattr(user, 'mesa'):
            login(request, user)
            return redirect('index')
        else:
            return HttpResponse("Usuario o contraseña inválidos o el usuario no es una mesa.")
    
    return render(request, 'login.html')


def logout_user(request):
    """Cierra la sesión de la mesa."""
    logout(request)
    return redirect('login')


def productos(request):
    """Muestra los productos para el administrador."""
    productos = Producto.objects.all()
    return render(request, 'productos.html', {'productos': productos})


def agregar_producto(request, producto_id):
    """Agrega un producto al pedido de la mesa."""
    producto = get_object_or_404(Producto, id=producto_id)
    cantidad = int(request.POST.get('cantidad', 1))

    if not hasattr(request.user, 'mesa'):
        return HttpResponse("Este usuario no tiene una mesa asignada.", status=400)

    mesa = request.user.mesa
    pedido, created = Pedido.objects.get_or_create(mesa=mesa, finalizado=False)
    detalle, created = DetallePedido.objects.get_or_create(pedido=pedido, producto=producto)
    detalle.cantidad += cantidad
    detalle.save()

    return redirect('index')

# Vista de administración principal
def admin_home(request):
    productos = Producto.objects.all()
    mesas = Mesa.objects.all()
    pedidos = Pedido.objects.all()
    return render(request, 'admin_home.html', {'productos': productos, 'mesas': mesas, 'pedidos': pedidos})

# Productos
def crear_producto(request):
    if request.method == "POST":
        Producto.objects.create(
            nombre=request.POST['nombre'],
            descripcion=request.POST.get('descripcion', ''),
            precio=request.POST['precio'],
            categoria=request.POST['categoria'],
            stock=request.POST['stock']
        )
        return redirect('admin_home')
    return render(request, 'crear_producto.html')

def editar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    if request.method == "POST":
        producto.nombre = request.POST['nombre']
        producto.descripcion = request.POST.get('descripcion', '')
        producto.precio = request.POST['precio']
        producto.categoria = request.POST['categoria']
        producto.stock = request.POST['stock']
        producto.save()
        return redirect('admin_home')
    return render(request, 'editar_producto.html', {'producto': producto})

def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    producto.delete()
    return redirect('admin_home')

# Mesas


def editar_mesa(request, mesa_id):
    mesa = get_object_or_404(Mesa, id=mesa_id)
    if request.method == "POST":
        mesa.numero = request.POST['numero']
        mesa.disponible = 'disponible' in request.POST
        mesa.save()
        return redirect('admin_home')
    return render(request, 'editar_mesa.html', {'mesa': mesa})

def eliminar_mesa(request, mesa_id):
    mesa = get_object_or_404(Mesa, id=mesa_id)
    mesa.delete()
    return redirect('admin_home')

# Pedidos (Detalles del Pedido)
def editar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    detalles = pedido.detalles.all()
    return render(request, 'editar_pedido.html', {'pedido': pedido, 'detalles': detalles})


from django.shortcuts import render, redirect, get_object_or_404
from .models import Mesa, Producto, Pedido, DetallePedido
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse

def admin_home(request):
    """Vista principal del administrador."""
    productos = Producto.objects.all()
    mesas = Mesa.objects.all()
    pedidos = Pedido.objects.all()
    return render(request, 'admin_home.html', {'productos': productos, 'mesas': mesas, 'pedidos': pedidos})

# Productos
def crear_producto(request):
    if request.method == "POST":
        Producto.objects.create(
            nombre=request.POST['nombre'],
            descripcion=request.POST.get('descripcion', ''),
            precio=request.POST['precio'],
            categoria=request.POST['categoria'],
            stock=request.POST['stock']
        )
        return redirect('admin_home')
    return render(request, 'crear_producto.html')

def editar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    if request.method == "POST":
        producto.nombre = request.POST['nombre']
        producto.descripcion = request.POST.get('descripcion', '')
        producto.precio = request.POST['precio']
        producto.categoria = request.POST['categoria']
        producto.stock = request.POST['stock']

        # Verifica si hay una nueva imagen cargada
        if 'imagen' in request.FILES:
            producto.imagen = request.FILES['imagen']  # Actualiza la imagen si se cargó una nueva

        producto.save()  # Guarda los cambios del producto, incluyendo la imagen actualizada
        return redirect('admin_home')
    return render(request, 'editar_producto.html', {'producto': producto})
def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    producto.delete()
    return redirect('admin_home')

# Mesas
def crear_mesa(request):
    if request.method == "POST":
        numero = request.POST.get('numero')
        Mesa.objects.create(numero=numero)
        return redirect('admin_home')  # Asegúrate de que esta URL esté configurada correctamente
    return render(request, 'crear_mesa.html')

def editar_mesa(request, mesa_id):
    mesa = get_object_or_404(Mesa, id=mesa_id)
    if request.method == "POST":
        mesa.numero = request.POST['numero']
        mesa.disponible = 'disponible' in request.POST
        mesa.save()
        return redirect('admin_home')
    return render(request, 'editar_mesa.html', {'mesa': mesa})

def eliminar_mesa(request, mesa_id):
    mesa = get_object_or_404(Mesa, id=mesa_id)
    mesa.delete()
    return redirect('admin_home')

# Pedidos
def editar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    detalles = pedido.detalles.all()
    return render(request, 'editar_pedido.html', {'pedido': pedido, 'detalles': detalles})

# Autenticación
def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        
        if user is not None and hasattr(user, 'mesa'):
            login(request, user)
            return redirect('index')
        else:
            return HttpResponse("Usuario o contraseña inválidos o el usuario no es una mesa.")
    
    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    return redirect('login')

# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Mesa

def admin_home(request):
    mesas = Mesa.objects.all()
    return render(request, 'admin_home.html', {'mesas': mesas})

# Vista para crear una mesa


# Vista para editar una mesa
def editar_mesa(request, mesa_id):
    mesa = get_object_or_404(Mesa, id=mesa_id)
    if request.method == "POST":
        mesa.numero = request.POST['numero']
        mesa.disponible = 'disponible' in request.POST
        mesa.save()
        return redirect('admin_home')
    return render(request, 'editar_mesa.html', {'mesa': mesa})

# Vista para eliminar una mesa
def eliminar_mesa(request, mesa_id):
    mesa = get_object_or_404(Mesa, id=mesa_id)
    if request.method == "POST":
        mesa.delete()
        return redirect('admin_home')
    return render(request, 'eliminar_mesa.html', {'mesa': mesa})

def admin_home(request):
    productos = Producto.objects.all()  # Consulta para obtener todos los productos
    mesas = Mesa.objects.all()  # Consulta para obtener todas las mesas
    return render(request, 'admin_home.html', {'productos': productos, 'mesas': mesas})
# views.py
def index(request):
    productos = Producto.objects.all()
    return render(request, 'index.html', {'productos': productos})

def login_mesa(request):
    if request.method == "POST":
        numero_mesa = request.POST.get("numero_mesa")
        
        try:
            mesa = Mesa.objects.get(numero=numero_mesa)
            request.session['mesa_id'] = mesa.id  # Guardamos la mesa en la sesión
            return redirect('index')  # Redirige al menú
        except Mesa.DoesNotExist:
            messages.error(request, "La mesa ingresada no existe.")
            return redirect('login_mesa')  # Redirige al inicio de sesión si la mesa no existe

    return render(request, 'login_mesa.html')

# views.py
from django.shortcuts import render, redirect
from .models import Producto, Mesa

def index(request):
    # Verificamos si la mesa está en la sesión
    if 'mesa_id' not in request.session:
        return redirect('login_mesa')  # Redirige al inicio de sesión de mesa si no está autenticado

    productos = Producto.objects.all()
    return render(request, 'index.html', {'productos': productos})

def pedido_resumen(request):
    pedido = Pedido.objects.last()  # El último pedido realizado
    return render(request, 'pedido_resumen.html', {'pedido': pedido})

# views.py
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Producto, Pedido, DetallePedido

def finalizar_pedido(request):
    if request.method == 'POST':
        carrito = request.session.get('cart', {})
        if not carrito:
            return JsonResponse({"error": "El carrito está vacío"}, status=400)

        total = sum(item['cantidad'] * item['precio'] for item in carrito.values())
        
        # Crear el pedido
        pedido = Pedido.objects.create(total=total)

        # Crear detalles del pedido
        for product_id, item in carrito.items():
            producto = Producto.objects.get(id=product_id)
            DetallePedido.objects.create(
                pedido=pedido,
                producto=producto,
                cantidad=item['cantidad'],
                precio=producto.precio
            )

        # Limpiar el carrito de la sesión
        request.session['cart'] = {}

        return render(request, 'pedido_resumen.html', {'pedido': pedido})
    
    return redirect('index')

# views.py
from django.shortcuts import render
from .models import Pedido

def ver_pedidos(request):
    """Vista que muestra todos los pedidos para el administrador."""
    pedidos = Pedido.objects.all()
    
    # Calcula el subtotal de cada detalle de pedido
    for pedido in pedidos:
        for detalle in pedido.detalles.all():
            detalle.subtotal = detalle.cantidad * detalle.precio

    return render(request, 'ver_pedidos.html', {'pedidos': pedidos})

# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Mesa, Producto, Pedido, DetallePedido
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Producto, Pedido, DetallePedido
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def guardar_pedido(request):
    if request.method == 'POST':
        # Parseamos el carrito enviado en formato JSON
        carrito = json.loads(request.body)
        
        # Validamos si el carrito está vacío
        if not carrito:
            return JsonResponse({"error": "El carrito está vacío"}, status=400)

        # Calculamos el total del pedido
        total = sum(item['quantity'] * item['price'] for item in carrito.values())
        
        # Creamos el pedido
        pedido = Pedido.objects.create(total=total)

        # Iteramos sobre los productos del carrito y actualizamos el stock
        for product_id, item in carrito.items():
            producto = Producto.objects.get(id=product_id)
            
            # Verificamos que el stock del producto sea suficiente
            if producto.stock < item['quantity']:
                return JsonResponse({"error": f"No hay suficiente stock para {producto.nombre}"}, status=400)

            # Creamos el detalle del pedido
            DetallePedido.objects.create(
                pedido=pedido,
                producto=producto,
                cantidad=item['quantity'],
                precio=producto.precio
            )

            # Reducimos el stock del producto en función de la cantidad solicitada
            producto.stock -= item['quantity']
            producto.save()  # Guardamos los cambios del stock en la base de datos

        # Limpiamos el carrito de la sesión (opcional)
        request.session['cart'] = {}

        # Respondemos con un mensaje de éxito
        return JsonResponse({"mensaje": "Pedido finalizado con éxito"})
    
    # Redirige al menú principal si no se usa el método POST
    return redirect('index')

# views.py
def ver_pedidos(request):
    pedidos = Pedido.objects.all()
    return render(request, 'ver_pedidos.html', {'pedidos': pedidos})

def actualizar_estado_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    if request.method == 'POST':
        nuevo_estado = request.POST.get('estado')
        if nuevo_estado in dict(Pedido.ESTADO_OPCIONES).keys():
            pedido.estado = nuevo_estado
            pedido.save()
    return redirect('ver_pedidos')

# views.py
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Producto, Pedido, DetallePedido, Mesa
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def guardar_pedido(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        mesa_id = request.session.get('mesa_id')

        if not mesa_id:
            return JsonResponse({"error": "Mesa no encontrada"}, status=400)

        mesa = Mesa.objects.get(id=mesa_id)
        total = sum(item['quantity'] * item['price'] for item in data.values())

        pedido = Pedido.objects.create(mesa=mesa, total=total, estado='no tomado')

        for product_id, item in data.items():
            producto = Producto.objects.get(id=product_id)
            DetallePedido.objects.create(
                pedido=pedido,
                producto=producto,
                cantidad=item['quantity'],
                precio=producto.precio
            )

        return JsonResponse({"mensaje": "Pedido guardado con éxito"})
    return JsonResponse({"error": "Método no permitido"}, status=405)

def ver_pedidos(request):
    pedidos = Pedido.objects.all()
    return render(request, 'ver_pedidos.html', {'pedidos': pedidos})

def actualizar_estado_pedido(request, pedido_id):
    pedido = Pedido.objects.get(id=pedido_id)
    if request.method == 'POST':
        estado = request.POST.get('estado')
        pedido.estado = estado
        pedido.save()
    return redirect('ver_pedidos')

# views.py
from django.shortcuts import render, get_object_or_404
from .models import Pedido, DetallePedido

from django.shortcuts import render, get_object_or_404
from .models import Pedido

def ver_detalle_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    detalles = pedido.detalles.all()
    
    # Calculate the total amount
    total = sum(detalle.cantidad * detalle.producto.precio for detalle in detalles)
    
    return render(request, 'detalle_pedido.html', {
        'pedido': pedido,
        'detalles': detalles,
        'total': total
    })


def eliminar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    pedido.delete()
    return redirect(reverse('ver_pedidos'))


def obtener_pedidos_actualizados(request):
    pedidos = Pedido.objects.values('id', 'mesa__numero', 'total', 'estado', 'fecha')
    return JsonResponse(list(pedidos), safe=False)

# Suponiendo que tienes una función de vista para crear un detalle de pedido

