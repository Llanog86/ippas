from django.db import models

class Usuario(models.Model):
    idusuario = models.AutoField(primary_key=True)
    usuario = models.CharField(max_length=100)
    contraseña = models.CharField(max_length=100)
    mail= models.EmailField()
    fecha = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        # Indica el nombre de la tabla existente en tu base de datos
        db_table = 'usuarios'
        
class Empresa(models.Model):
    cuit = models.CharField(max_length=11, primary_key=True)
    usuario = models.CharField(max_length=100)
    razon_soc_emp = models.CharField(max_length=100)
    domicilio = models.CharField(max_length=100)
    provincia = models.CharField(max_length=100)
    cond_impos = models.CharField(max_length=20)
    CAE = models.CharField(max_length=50)
    moneda = models.CharField(max_length=10)

    class Meta:
        # Indica el nombre de la tabla existente en tu base de datos
        db_table = 'empresa'
        
class Provincia(models.Model):
    Cod_provincia = models.CharField(max_length=2, primary_key=True)
    Des_provincia = models.CharField(max_length=100)

    def __str__(self):
        return self.Des_provincia
    
    class Meta:
        db_table = 'provincias'
        
class CondImpos(models.Model):
    id_Cond = models.CharField(max_length=2, primary_key=True)
    Des_Condicion = models.CharField(max_length=100)

    def __str__(self):
        return self.Des_Condicion
    
    class Meta:
        db_table = 'cond_impositiva'

class Moneda(models.Model):
    idmoneda = models.CharField(max_length=2, primary_key=True)
    cod_moneda = models.CharField(max_length=10)
    des_moneda = models.CharField(max_length=50)

    def __str__(self):
        return self.cod_moneda
    
    class Meta:
        db_table = 'moneda'

class Clientes(models.Model):
    cod_cliente = models.CharField(max_length=11, primary_key=True)
    cuit_empresa = models.CharField(max_length=100)
    cuit = models.CharField(max_length=100)
    razon_social = models.CharField(max_length=100)
    cond_impos = models.CharField(max_length=100)
    domicilio = models.CharField(max_length=20)
    provincia = models.CharField(max_length=50)
    moneda = models.CharField(max_length=10)
    actividad = models.CharField(max_length=20)
    contacto = models.EmailField()
    telefono = models.CharField(max_length=50)

    class Meta:
        # Indica el nombre de la tabla existente en tu base de datos
        db_table = 'clientes'