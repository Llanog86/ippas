from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib import messages
from .models import * # Importa tu modelo de usuario aquí
from django.core.mail import send_mail
import pandas as pd


def registro_usuario(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        
        # Verificar si el usuario ya existe
        if Usuario.objects.filter(usuario=username).exists():
            mensaje = "El usuario ya se encuentra registrado."
        else:
            # Crear el usuario y guardarlo en la base de datos
            nuevo_usuario = Usuario(usuario=username, contraseña=password, mail=email)
            nuevo_usuario.save()
            mensaje = "Usuario creado correctamente."
        
        return render(request, 'registro.html', {'mensaje': mensaje})
    else:
        return render(request, 'registro.html')

def iniciar_sesion(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        try:
            # Obtener el usuario de la base de datos
            usuario = Usuario.objects.get(usuario=username)
            
            # Verificar si la contraseña coincide
            if usuario.contraseña == password:
                # Si coincide, iniciar sesión y redirigir a la página de bienvenida
                request.session['usuario_id'] = usuario.idusuario  # Guardar el ID del usuario en la sesión
                return redirect('bienvenida')
            else:
                # Si la contraseña no coincide, mostrar un mensaje de error
                messages.error(request, 'Usuario o contraseña incorrectos.')
        except Usuario.DoesNotExist:
            # Si el usuario no existe, mostrar un mensaje de error
            messages.error(request, 'Usuario o contraseña incorrectos.')
    
    # Renderizar la plantilla de inicio de sesión
    return render(request, 'login.html')

def pagina_bienvenida(request):
    # Verificar si el usuario está autenticado
    if 'usuario_id' in request.session:
        # Obtener el ID del usuario de la sesión
        usuario_id = request.session['usuario_id']
        # Obtener el usuario de la base de datos utilizando el ID
        usuario = Usuario.objects.get(idusuario=usuario_id)
        return render(request, 'Bienvenido.html', {'usuario': usuario})
    else:
        # Si el usuario no está autenticado, redirigir a la página de inicio de sesión
        return redirect('login')

def cerrar_sesion(request):
    logout(request)
    return redirect('login')

def recuperar_contrasena(request):
    mensaje = None
    if request.method == 'POST':
        email = request.POST['email']
        try:
            usuario = Usuario.objects.get(mail=email)  # Cambia User por Usuario
            password = usuario.contraseña  # Obtén la contraseña del usuario
            # Envía el correo con la contraseña recuperada
            send_mail(
                'Recuperación de Contraseña',
                f'Tu contraseña es: {password}',
                'tu_correo@gmail.com',
                [email],
                fail_silently=False,
            )
            mensaje = 'Se ha enviado un correo electrónico con la contraseña.'
        except Usuario.DoesNotExist:
            mensaje = 'El correo ingresado no existe en la base de datos.'
    
    return render(request, 'recupero.html', {'mensaje': mensaje})

def perfil_empresa(request):
    usuario_id = request.session.get('usuario_id')
    usuario = None
    empresas = None
    provincias = Provincia.objects.all()
    condimpos = CondImpos.objects.all()
    moneda = Moneda.objects.all()

    if usuario_id:
        try:
            usuario = Usuario.objects.get(idusuario=usuario_id)
        except Usuario.DoesNotExist:
            pass

    if usuario:
        empresas = Empresa.objects.filter(usuario=usuario.usuario)

    if request.method == 'POST':
        cuit = request.POST.get('cuit')
        usuario = request.POST.get('usuario')
        razon_soc_emp = request.POST.get('razon_soc_emp')
        domicilio = request.POST.get('domicilio')
        provincia = request.POST.get('provincia')
        cond_impos = request.POST.get('condimpos')
        CAE = request.POST.get('CAE')
        moneda = request.POST.get('moneda')

        try:
            # Intentar obtener la empresa existente con el CUIT proporcionado
            empresa_existente = Empresa.objects.get(cuit=cuit)

            # Actualizar los datos si la empresa existe
            empresa_existente.usuario = usuario
            empresa_existente.razon_soc_emp = razon_soc_emp
            empresa_existente.domicilio = domicilio
            empresa_existente.provincia = provincia
            empresa_existente.cond_impos = cond_impos
            empresa_existente.CAE = CAE
            empresa_existente.moneda = moneda
            empresa_existente.save()

            # Mostrar mensaje de éxito de actualización
            messages.success(request, 'Los datos de la empresa fueron actualizados correctamente!')
        except Empresa.DoesNotExist:
            # Si la empresa no existe, crear una nueva
            Empresa.objects.create(
                cuit=cuit,
                usuario=usuario,
                razon_soc_emp=razon_soc_emp,
                domicilio=domicilio,
                provincia=provincia,
                cond_impos=cond_impos,
                CAE=CAE,
                moneda=moneda,
            )

            # Mostrar mensaje de éxito de creación
            messages.success(request, 'La empresa fue registrada correctamente!')

        return redirect('Perfil')

    return render(request, 'Perfil.html', {'empresas': empresas, 'provincias': provincias, 'usuario': usuario, 'condimpos': condimpos, 'moneda': moneda})

def baja_empresa(request, cuit):
    # Buscar la compañía por su código
    try:
        empresa = Empresa.objects.get(cuit=cuit)
    except Empresa.DoesNotExist:
        return render(request, 'error.html', {'mensaje': 'La compañía no existe'})

    # Anular la compañía (eliminarla de la base de datos)
    empresa.delete()

    # Redirigir a la página de compañías registradas con un mensaje de éxito
    return redirect('Perfil')

def process_excel_data(file):
    df = pd.read_excel(file)
    for index, row in df.iterrows():
        cod_cliente = row['cod_cliente']
        cuit_empresa = row['cuit_empresa']
        cuit = row['cuit']
        razon_social = row['razon_social']
        cond_impos = row['cond_impos']
        domicilio = row['domicilio']
        provincia = row['provincia']
        moneda = row['moneda']
        actividad = row['actividad']
        contacto = row['contacto']
        telefono = row['telefono']
        # Crea o actualiza el cliente según sea necesario
        cliente_existente = Clientes.objects.filter(cuit=cuit).first()
        if cliente_existente:
            cliente_existente.cod_cliente = cod_cliente
            cliente_existente.cuit_empresa = cuit_empresa
            cliente_existente.razon_social = razon_social
            cliente_existente.cond_impos = cond_impos
            cliente_existente.domicilio = domicilio
            cliente_existente.provincia = provincia
            cliente_existente.moneda = moneda
            cliente_existente.actividad = actividad
            cliente_existente.contacto = contacto
            cliente_existente.telefono = telefono
            cliente_existente.save()
        else:
            nuevo_cliente = Clientes.objects.create(
                cod_cliente=cod_cliente,
                cuit_empresa=cuit_empresa,
                cuit=cuit,
                razon_social=razon_social,
                cond_impos=cond_impos,
                domicilio=domicilio,
                provincia=provincia,
                moneda=moneda,
                actividad=actividad,
                contacto=contacto,
                telefono=telefono
            )
                
def registrar_cliente(request):
    
    if request.method == 'POST':
        if 'fileInput' in request.FILES:
            file = request.FILES['fileInput']
            process_excel_data(file)
            messages.success(request, 'Datos del archivo Excel procesados y guardados exitosamente.')
            return redirect('Clientes')
        else:
            # Procesa los datos del formulario si no se ha subido un archivo
            pass
    
    # Obtener el usuario autenticado y logeado
    usuario_id = request.session.get('usuario_id')
    usuario = None
    empresa = None
    
    if usuario_id:
        try:
            usuario = Usuario.objects.get(idusuario=usuario_id)
        except Usuario.DoesNotExist:
            pass

    if usuario:
        # Filtrar las empresas asociadas al usuario autenticado
        empresas = Empresa.objects.filter(usuario=usuario.usuario)
        # Obtener los cuit de las empresas asociadas al usuario autenticado
        cuit_empresas = empresas.values_list('cuit', flat=True)
    
    provincias = Provincia.objects.all()
    condimpos = CondImpos.objects.all()
    moneda = Moneda.objects.all()

    if request.method == 'POST':
        cod_cliente = request.POST.get('cod_cliente')
        cuit_empresa = request.POST.get('cuit_empresa')
        cuit = request.POST.get('cuit')
        razon_social = request.POST.get('razon_social')
        cond_impos = request.POST.get('cond_impos')
        domicilio = request.POST.get('domicilio')
        provincia = request.POST.get('provincia')
        moneda = request.POST.get('moneda')
        actividad = request.POST.get('actividad')
        contacto = request.POST.get('contacto')
        telefono= request.POST.get('telefono')
        
        # Verificar si se han proporcionado todos los datos necesarios
        if not (cod_cliente and cuit_empresa and cuit and razon_social and cond_impos and domicilio and provincia and moneda and actividad and contacto and telefono):
            # Si faltan datos, mostrar un mensaje de error
            messages.error(request, 'Por favor, ingrese todos los datos solicitados.')
            return redirect('Clientes')


        # Buscar si el cliente ya existe
        cliente_existente = Clientes.objects.filter(cuit=cuit).first()

        if cliente_existente:
            # Si el cliente existe, actualiza los datos
            cliente_existente.cod_cliente = cod_cliente
            cliente_existente.cuit_empresa = cuit_empresa
            cliente_existente.razon_social = razon_social
            cliente_existente.cond_impos = cond_impos
            cliente_existente.domicilio = domicilio
            cliente_existente.provincia = provincia
            cliente_existente.moneda = moneda
            cliente_existente.actividad = actividad
            cliente_existente.contacto = contacto
            cliente_existente.telefono = telefono
            cliente_existente.save()

            # Mostrar mensaje de éxito de actualización
            messages.success(request, f'Los datos del cliente {cliente_existente.cod_cliente} fueron actualizados.')
        else:
            # Si el cliente no existe, crear uno nuevo
            nuevo_cliente = Clientes.objects.create(
                cod_cliente = cod_cliente,
                cuit_empresa=cuit_empresa,
                cuit=cuit,
                razon_social=razon_social,
                cond_impos=cond_impos,
                domicilio=domicilio,
                provincia=provincia,
                moneda=moneda,
                actividad=actividad,
                contacto=contacto,
                telefono=telefono
            )

            # Mostrar mensaje de éxito de creación
            messages.success(request, f'El cliente fue registrado exitosamente para la empresa {cuit_empresa}.')

        return redirect('Clientes')

    return render(request, 'Clientes.html', {'provincias': provincias, 'condimpos': condimpos, 'moneda': moneda, 'cuit_empresas': cuit_empresas, 'empresas': empresas })

def consulta_clientes(request):
    # Obtener el usuario autenticado y logeado
    usuario_id = request.session.get('usuario_id')
    usuario = None
    mensaje = None
    clientes = None
    
    if usuario_id:
        try:
            usuario = Usuario.objects.get(idusuario=usuario_id)
        except Usuario.DoesNotExist:
            pass

    if usuario:
        # Filtrar las empresas asociadas al usuario autenticado
        empresas = Empresa.objects.filter(usuario=usuario.usuario)
        # Obtener los cuit de las empresas asociadas al usuario autenticado
        cuit_empresas = empresas.values_list('cuit', flat=True)
        
        # Realizar la búsqueda basada en los parámetros proporcionados
        if request.method == 'GET':
            codigo_cliente = request.GET.get('codigo_cliente')
            nombre = request.GET.get('nombre')
            cuit = request.GET.get('cuit')
            cuit_empresa = request.GET.get('cuit_empresa')

            # Verificar la opción de búsqueda seleccionada
            if request.GET.get('search-type') == 'client':
                # Búsqueda por datos de cliente
                if codigo_cliente or nombre or cuit:
                    clientes = Clientes.objects.filter(cuit_empresa__in=cuit_empresas)

                    if codigo_cliente:
                        clientes = clientes.filter(cod_cliente__icontains=codigo_cliente)
                    elif nombre:
                        clientes = clientes.filter(razon_social__icontains=nombre)
                    elif cuit:
                        clientes = clientes.filter(cuit__icontains=cuit)
                else:
                    mensaje = "Por favor, ingrese al menos un dato del cliente para buscar."
            elif request.GET.get('search-type') == 'company':
                # Búsqueda por CUIT de empresa
                # Solo permitir la búsqueda si el usuario autenticado tiene acceso a la empresa
                if cuit_empresa in cuit_empresas:
                    clientes = Clientes.objects.filter(cuit_empresa=cuit_empresa)
                else:
                    mensaje = "La empresa buscada no existe."

            # Verificar si se encontraron resultados
            if clientes is not None and not clientes.exists():
                mensaje = "El cliente buscado no existe."

    return render(request, 'consulta_clientes.html', {'clientes': clientes, 'mensaje': mensaje})






