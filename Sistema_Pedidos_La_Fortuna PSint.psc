Algoritmo Sistema_Pedidos_La_Fortuna
	Definir total, opcion, platoOpc, pagoOpc Como Entero
	Definir i, posicion, cantidad, nuevoEstado Como Entero
	Definir codigo, cliente, dni, producto, observacion, formaPago Como Cadena
	Definir confirmar Como Cadena
	Definir duplicado Como Lógico
	Definir precio, subtotal Como Real
	Dimensionar codigos(100)
	Dimensionar clientes(100)
	Dimensionar dnis(100)
	Dimensionar productos(100)
	Dimensionar cantidades(100)
	Dimensionar precios(100)
	Dimensionar subtotales(100)
	Dimensionar observaciones(100)
	Dimensionar estados(100)
	Dimensionar formasPago(100)
	total <- 0
	Repetir
		Escribir ''
		Escribir '================================================'
		Escribir '    RESTAURANTE Y POLLERIA LA FORTUNA'
		Escribir '        SISTEMA DE CONTROL DE ALMUERZOS'
		Escribir '================================================'
		Escribir ' 1. Registrar un pedido'
		Escribir ' 2. Consultar un pedido'
		Escribir ' 3. Mostrar todos los pedidos'
		Escribir ' 4. Actualizar estado del pedido'
		Escribir ' 5. Contar pedidos registrados'
		Escribir ' 6. Salir'
		Escribir '================================================'
		Escribir 'Selecciona una opcion (1-6):'
		Leer opcion
		Según opcion Hacer
	1:
		Escribir ''
		Escribir '--- REGISTRAR PEDIDO ---'
		Si total<100 Entonces
			Escribir 'Nombre completo del cliente:'
			Leer cliente
			Escribir 'DNI del cliente (8 digitos):'
			Leer dni
			Escribir ''
			Escribir '--- MENU DE ALMUERZOS ---'
			Escribir '1. Arroz con pollo (S/ 12.00)'
			Escribir '2. Lomo saltado (S/ 15.00)'
			Escribir '3. Pollo a la plancha (S/ 13.00)'
			Escribir '4. Tallarin saltado (S/ 12.00)'
			Escribir '5. Caldo de gallina (S/ 12.00)'
			Escribir '6. Milanesa de pollo (S/ 14.00)'
			Escribir '7. Seco de res con frejoles (S/ 15.00)'
			Escribir '8. Aji de gallina (S/ 12.00)'
			Escribir 'Selecciona el numero del plato (1-8):'
			Leer platoOpc
			Según platoOpc Hacer
		1:
			producto <- 'Arroz con pollo'
			precio <- 12.00
		2:
			producto <- 'Lomo saltado'
			precio <- 15.00
		3:
			producto <- 'Pollo a la plancha'
			precio <- 13.00
		4:
			producto <- 'Tallarin saltado'
			precio <- 12.00
		5:
			producto <- 'Caldo de gallina'
			precio <- 12.00
		6:
			producto <- 'Milanesa de pollo'
			precio <- 14.00
		7:
			producto <- 'Seco de res con frejoles'
			precio <- 15.00
		8:
			producto <- 'Aji de gallina'
			precio <- 12.00
		De Otro Modo:
			producto <- 'Plato general'
			precio <- 12.00
	FinSegún
	Escribir 'Cantidad de platos:'
	Leer cantidad
	Escribir 'Selecciona la forma de pago:'
	Escribir '1. Yape'
	Escribir '2. Efectivo'
	Escribir '3. Plin'
	Leer pagoOpc
	Según pagoOpc Hacer
1:
	formaPago <- 'Yape'
2:
	formaPago <- 'Efectivo'
3:
	formaPago <- 'Plin'
De Otro Modo:
	formaPago <- 'Efectivo'
FinSegún
Si cliente<>'' Y dni<>'' Y cantidad>0 Entonces
	duplicado <- Falso
	Para i<-1 Hasta total Hacer
		Si Mayusculas(clientes[i])=Mayusculas(cliente) Y Mayusculas(productos[i])=Mayusculas(producto) Y estados[i]<>'Atendido' Entonces
			duplicado <- Verdadero
		FinSi
	FinPara
	Si duplicado=Verdadero Entonces
		Escribir 'Advertencia: existe un pedido similar pendiente.'
		Escribir 'Deseas registrar el pedido? Escribe S o N:'
		Leer confirmar
	SiNo
		confirmar <- 'S'
	FinSi
	Si Mayusculas(confirmar)='S' Entonces
		total <- total+1
		Si total<10 Entonces
			codigo <- Concatenar('F000',ConvertirATexto(total))
		SiNo
			Si total<100 Entonces
				codigo <- Concatenar('F00',ConvertirATexto(total))
			SiNo
				codigo <- Concatenar('F0',ConvertirATexto(total))
			FinSi
		FinSi
		subtotal <- precio*cantidad
		codigos[total] <- codigo
		clientes[total] <- cliente
		dnis[total] <- dni
		productos[total] <- producto
		cantidades[total] <- cantidad
		precios[total] <- precio
		subtotales[total] <- subtotal
		formasPago[total] <- formaPago
		estados[total] <- 'Pendiente'
		Escribir 'Observaciones (Enter o escribe SIN si no hay):'
		Leer observacion
		Si observacion='' Entonces
			observacion <- 'Sin observaciones'
		FinSi
		observaciones[total] <- observacion
		Escribir ''
		Escribir '=============================================='
		Escribir '          ¡PEDIDO REGISTRADO EXITOSAMENTE!'
		Escribir '=============================================='
		Escribir ' Codigo asignado:    ', codigos[total]
		Escribir ' Cliente:            ', clientes[total]
		Escribir ' DNI:                ', dnis[total]
		Escribir ' Plato:              ', productos[total]
		Escribir ' Precio unitario:    S/ ', precios[total]
		Escribir ' Cantidad:           ', cantidades[total]
		Escribir ' Forma de pago:      ', formasPago[total]
		Escribir ' Total a pagar:      S/ ', subtotales[total]
		Escribir ' Observaciones:      ', observaciones[total]
		Escribir ' Estado:             Pendiente'
		Escribir '=============================================='
	SiNo
		Escribir 'Registro cancelado por el usuario.'
	FinSi
SiNo
	Escribir 'Error: verifica los datos ingresados.'
FinSi
SiNo
	Escribir 'Se alcanzo el limite maximo de 100 pedidos.'
FinSi
2:
	Escribir ''
	Escribir '--- CONSULTAR PEDIDO ---'
	Escribir 'Ingresa el codigo del pedido (ej. F0001):'
	Leer codigo
	posicion <- 0
	Para i<-1 Hasta total Hacer
		Si Mayusculas(codigos[i])=Mayusculas(codigo) Entonces
			posicion <- i
		FinSi
	FinPara
	Si posicion=0 Entonces
		Escribir 'No se encontro ningun pedido con el codigo ', codigo
	SiNo
		Escribir ''
		Escribir '========== DATOS DEL PEDIDO =========='
		Escribir 'Codigo:        ', codigos[posicion]
		Escribir 'Cliente:       ', clientes[posicion]
		Escribir 'DNI:           ', dnis[posicion]
		Escribir 'Plato:         ', productos[posicion]
		Escribir 'Precio unit.:  S/ ', precios[posicion]
		Escribir 'Cantidad:      ', cantidades[posicion]
		Escribir 'Total a pagar: S/ ', subtotales[posicion]
		Escribir 'Forma de pago: ', formasPago[posicion]
		Escribir 'Observaciones: ', observaciones[posicion]
		Escribir 'Estado:        ', estados[posicion]
		Escribir '======================================'
	FinSi
3:
	Escribir ''
	Escribir '--- LISTA DE TODOS LOS PEDIDOS ---'
	Si total=0 Entonces
		Escribir 'Todavia no hay pedidos registrados en el sistema.'
	SiNo
		Para i<-1 Hasta total Hacer
			Escribir '--------------------------------------'
			Escribir 'Codigo:        ', codigos[i]
			Escribir 'Cliente:       ', clientes[i]
			Escribir 'DNI:           ', dnis[i]
			Escribir 'Plato:         ', productos[i]
			Escribir 'Total:         S/ ', subtotales[i]
			Escribir 'Pago:          ', formasPago[i]
			Escribir 'Estado:        ', estados[i]
		FinPara
		Escribir '--------------------------------------'
	FinSi
4:
	Escribir ''
	Escribir '--- ACTUALIZAR ESTADO DEL PEDIDO ---'
	Escribir 'Ingresa el codigo del pedido a actualizar:'
	Leer codigo
	posicion <- 0
	Para i<-1 Hasta total Hacer
		Si Mayusculas(codigos[i])=Mayusculas(codigo) Entonces
			posicion <- i
		FinSi
	FinPara
	Si posicion=0 Entonces
		Escribir 'No se encontro el pedido con el codigo ', codigo
	SiNo
		Escribir 'Estado actual: ', estados[posicion]
		Escribir 'Selecciona el nuevo estado:'
		Escribir '1. Pendiente'
		Escribir '2. En preparacion'
		Escribir '3. Atendido'
		Leer nuevoEstado
		Según nuevoEstado Hacer
	1:
		estados[posicion] <- 'Pendiente'
		Escribir 'Estado actualizado a: Pendiente'
	2:
		estados[posicion] <- 'En preparacion'
		Escribir 'Estado actualizado a: En preparacion'
	3:
		estados[posicion] <- 'Atendido'
		Escribir 'Estado actualizado a: Atendido'
	De Otro Modo:
		Escribir 'Opcion de estado no valida.'
FinSegún
FinSi
5:
	Escribir ''
	Escribir '======================================='
	Escribir ' TOTAL DE PEDIDOS REGISTRADOS: ', total
	Escribir '======================================='
6:
	Escribir ''
	Escribir '¡Gracias por utilizar el sistema de La Fortuna!'
De Otro Modo:
	Escribir 'Opcion no valida. Selecciona un numero entre 1 y 6.'
FinSegún
Hasta Que opcion=7
FinAlgoritmo