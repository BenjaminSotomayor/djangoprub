from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import render
# models.py
from django.db import models

class Mesa(models.Model):
    numero = models.PositiveIntegerField(unique=True)  # Número de la mesa, debe ser único
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)  # Usuario asociado a la mesa, puede ser nulo

    def __str__(self):
        return f"Mesa {self.numero}"


class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.CharField(
        max_length=50,
        choices=[('bebidas', 'Bebidas'), ('postres', 'Postres'), ('platos', 'Platos')]
    )
    stock = models.PositiveIntegerField(default=0)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)  # Campo para imagen

    def __str__(self):
        return self.nombre


class Pedido(models.Model):
    """Modelo que representa un pedido realizado por una mesa."""
    ESTADO_PEDIDO = [
        ('no tomado', 'No tomado'),
        ('en preparacion', 'En preparación'),
        ('servido', 'Servido')
    ]

    mesa = models.ForeignKey(Mesa, on_delete=models.CASCADE)  # Mesa que realiza el pedido
    estado = models.CharField(max_length=20, choices=ESTADO_PEDIDO, default='no tomado')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Usuario asociado al pedido
    fecha = models.DateTimeField(auto_now_add=True)  # Fecha de creación del pedido

    def __str__(self):
        return f"Pedido {self.id} en {self.mesa} por {self.usuario.username if self.usuario else 'Usuario no asignado'}"

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    precio = models.IntegerField()  # Cambiado a IntegerField
    categoria = models.CharField(
        max_length=50,
        choices=[
            ('bebidas', 'Bebidas'),
            ('postres', 'Postres'),
            ('platos', 'Platos')
        ]
    )
    stock = models.PositiveIntegerField(default=0)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)

    def __str__(self):
        return self.nombre



class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='detalles', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio = models.IntegerField() 

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre} en Pedido {self.pedido.id}"
    
    
