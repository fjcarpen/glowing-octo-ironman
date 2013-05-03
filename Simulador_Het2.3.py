import random
import math
#Necesito: Dimensiones(ejex-ejey):Centro Urbano:Centro(ejex-ejey):Radio(kms):
#TiposEscuela(Identificador-NumeroSalas-NumeroTurnos-Multiseriada(M)/Simple(S))Zona(Urbana,Rural)-TipoEsc(Identificador)-Cantidad(Nro)

class Paradero:
	def __init__(self, centro, rmin, rmax, arealocal, densidad_alumnos, cantidad_cursos, identescuela, max_students_fake_bus_stop):
		self.arealocal=arealocal
		self.centro=centro
		self.rmin=rmin
		self.rmax=rmax
		radio=random.uniform(rmin, rmax)
		angulo=random.uniform(0,math.radians(360))
		self.ubicacionx=radio*math.cos(angulo)+centro[0]
		self.ubicaciony=radio*math.sin(angulo)+centro[1]
		self.total_alumnos=densidad_alumnos
		alumnosrestantes=self.total_alumnos
		self.alumnos=[]
		self.cantidad_cursos=int(cantidad_cursos)
		self.identescuela=identescuela
		self.bus_stop_id=0
		self.stop_id=0
		self.max_students_fake_bus_stop=int(max_students_fake_bus_stop)
		self.fakebusstops=[]
		self.inroute=False


	def Set_total_alumnos(self, total_alumnos):
		self.total_alumnos=total_alumnos
		i=0
		for i in range(0,self.cantidad_cursos):
			self.alumnos.append(0)
		for i in range(0,self.total_alumnos):
			numerocurso=random.randint(0,self.cantidad_cursos-1)
			self.alumnos[numerocurso]=self.alumnos[numerocurso]+1

	def Set_bus_stop_id(self, bus_stop_id):
		self.bus_stop_id=bus_stop_id

	def Set_stop_id(self, stop_id):
		self.stop_id=stop_id

	def create_fakebusstops(self):

		i=1
		for cursos in self.alumnos:
			aux=int(cursos)
			while aux>=self.max_students_fake_bus_stop:
				self.fakebusstops.append(fake_bus_stop(self.identescuela, self.stop_id, self.bus_stop_id, self.max_students_fake_bus_stop, i))
				aux=aux-self.max_students_fake_bus_stop
			if aux>0:
				self.fakebusstops.append(fake_bus_stop(self.identescuela, self.stop_id, self.bus_stop_id, aux, i))
			i=i+1


class fake_bus_stop:
	def __init__(self, school_id, stop_id, bus_stop_id, students, grade):
		self.fake_bus_stop_id=0
		self.grade=grade
		self.students=students
		self.shift=0
		self.bus_stop_id=bus_stop_id
		self.stop_id=stop_id
		self.school_id=school_id
		self.inroute=False

	def Set_fake_busstop_id(self, fake_bus_stop_id):
		self.fake_bus_stop_id=fake_bus_stop_id

class Escuela:
	def __init__(self, ident, centrox, centroy, radio, xmax, ymax, a, a0, multiseriada, urbana, turnos, cantidad_salas, cantidad_alumnos, proporcion_ocupacion, max_students_fake_bus_stop, posx, posy, radiomax):
		self.ident=ident
		self.urbana= urbana
		if self.urbana==0:
			angulo= random.uniform(0, math.radians(360))
			radion= random.uniform(0, radio)	
			self.ubicacionx= centrox+radion*math.cos(angulo)
			self.ubicaciony=centroy+radion*math.sin(angulo)
		elif self.urbana==1:
			while True:
				self.ubicacionx=random.uniform(0, xmax)
				self.ubicaciony=random.uniform(0, ymax)
				if (math.pow(self.ubicacionx-centrox,2)+math.pow(self.ubicaciony-centroy,2))>radio:
					break
		else:
			self.ubicacionx=posx
			self.ubicaciony=posy

		self.rmax=min(radiomax, a0/a)
		self.cantidad_alumnos=cantidad_alumnos
		self.a=a
		self.a0=a0
		self.Area= -(math.exp(self.a0-self.a*self.rmax)/self.a)+(math.exp(self.a0)/self.a)
		self.paraderos=[]
		self.centro=[self.ubicacionx, self.ubicaciony]
		self.multiseriada=multiseriada
		if multiseriada:
			self.cantidad_cursos=7
		else:
			self.cantidad_cursos=11
		self.stop_id=0
		self.max_students_fake_bus_stop=max_students_fake_bus_stop
		self.proporcion_ocupacion=proporcion_ocupacion
		self.cantidad_salas=cantidad_salas
		self.turnos=turnos
		self.routes=[]
		self.bus_stop_id=0
		self.cantidad_real=0

	def Create_busstops(self):
		i=int(self.rmax)
		arealocal=0
		u=0
		areaacum=0
		paraderosaux=[]

		dist_entre_paraderos = 0.2
		
		self.paraderos.append(Paradero( self.centro, 0, 0, -(math.exp(self.a0-self.a*1)/self.a)+(math.exp(self.a0-self.a*(0))/self.a), math.exp(self.a0), self.cantidad_cursos, self.ident, self.max_students_fake_bus_stop))

		while(i>1):
			arealocal=-(math.exp(self.a0-self.a*i)/self.a)+(math.exp(self.a0-self.a*(i-dist_entre_paraderos))/self.a)
			areaacum=areaacum+arealocal
			densidad_alumnos=math.exp(self.a0-self.a*i)
			u=random.uniform(0, self.Area)
			if(areaacum>u):
				paraderoi= Paradero(self.centro,i-dist_entre_paraderos,i, arealocal, densidad_alumnos, self.cantidad_cursos, self.ident, self.max_students_fake_bus_stop)
				self.paraderos.append(paraderoi)
			i=i-dist_entre_paraderos
		for aux in range(1,len(self.paraderos)):
			for aux2 in range(0, len(self.paraderos)-aux):
				if self.paraderos[aux2].total_alumnos<self.paraderos[aux2+1].total_alumnos:
					aux3=self.paraderos[aux2]
					self.paraderos[aux2]=self.paraderos[aux2+1]
					self.paraderos[aux2+1]=aux3

	def Set_school_number_of_students(self):
		#sirve para hacer que el total de alumnos de la escuela quede en un paradero, para hacer las escuelas al porcentaje de capacidad indicado.
		totalum=0
		for paradero in self.paraderos:
			totalum=totalum+paradero.total_alumnos
		for paradero in self.paraderos:
			paradero.Set_total_alumnos(int(paradero.total_alumnos*self.cantidad_alumnos*self.cantidad_salas*self.turnos*self.proporcion_ocupacion/totalum))		
		#areaacum=0
		#for paradero in self.paraderos:
		#	areaacum=areaacum+paradero.arealocal
		#for paradero in self.paraderos:
		#	paradero.Set_total_alumnos(int(paradero.arealocal*self.cantidad_alumnos*self.proporcion_ocupacion/areaacum))
	
	def Set_stop_id(self, stop_id):
		self.stop_id=stop_id

class Municipalidad:
	def __init__(self, buscapacity):
		self.escuelas=[]
		self.stop=[]
		#(stop_id, latitude(y), longitude(x), urbano o rural(urban/rural))
		self.distance=[]
		#(stop_1_id, stop_2_id, distance)
		self.busstop=[]
		#(busstop_id, stop_id, initial_school_id)
		self.grade_busstop=[]
		#(stop_id, initial_school_id, grade_id, total_students)
		self.school=[]
		#(school_id, stop_id, classrooms)
		self.fakebusstop=[]
		#(fakebusstop_id, busstop_id, grade_id, students)
		self.buscapacity=int(buscapacity)
		self.routes=[]
		#(school_id, shift_id, route_id, fakebusstop_id, orden)
		self.sol_fakebusstop_shifts=[]
		#(fakebusstop_id, school_id, busstop_id, shift_id)
		self.sol_shift_programming=[]
		#school_id,shift_id,grade_id,operating_classrooms

	def crearescuelas(self, datosescuelas, centrox, centroy, radio, xmax, ymax, max_students_fake_bus_stop):
		for escuela in datosescuelas:
			i=len(self.escuelas)+1
			#escuela=[a, a0, multiseriada, urbana, turnos, cantidad_salas, cantidad_alumnos, proporcion_ocupacion, posx, posy, rmax]
			self.escuelas.append(Escuela(i, centrox, centroy, radio, xmax, ymax, escuela[0], escuela[1], escuela[2], escuela[3], escuela[4], escuela[5], escuela[6], escuela[7], max_students_fake_bus_stop, escuela[8], escuela[9], escuela[10]))
		for escuela in self.escuelas:
			escuela.Create_busstops()
			escuela.Set_school_number_of_students()
		i=1
		for escuela in self.escuelas:
			for paradero in escuela.paraderos:
				paradero.Set_bus_stop_id(i)
				paradero.Set_stop_id(i)
				#el stop id y bus stop id de las escuelas va asociado al paradero que esta a distancia 0 de esta.
				i=i+1
		for escuela in self.escuelas:
			for paradero in escuela.paraderos:
				paradero.create_fakebusstops()
		i=1
		for escuela in self.escuelas:
			for paradero in escuela.paraderos:
				for fakebusstop in paradero.fakebusstops:
					fakebusstop.Set_fake_busstop_id(i)
					i=i+1		

	def tables(self):
		for school in self.escuelas:
			for busstop in school.paraderos:
				aux=[busstop.stop_id, busstop.ubicaciony, busstop.ubicacionx]
				self.stop.append(aux)
		for school in self.escuelas:
			for busstop in school.paraderos:
				for school2 in self.escuelas:
					for busstop2 in school2.paraderos:
						aux=[busstop.stop_id, busstop2.stop_id, math.sqrt(math.pow(busstop.ubicacionx-busstop2.ubicacionx,2)+math.pow(busstop.ubicaciony-busstop2.ubicaciony,2))]
						self.distance.append(aux)
		for school in self.escuelas:
			for busstop in school.paraderos:
				aux=[busstop.bus_stop_id, busstop.stop_id, busstop.identescuela]
				self.busstop.append(aux)
		for school in self.escuelas:
			for busstop in school.paraderos:
				i=0
				for grade in busstop.alumnos:
					i=i+1
					if grade > 0:
						aux=[busstop.stop_id, busstop.identescuela, i, grade]
						self.grade_busstop.append(aux)
		for school in self.escuelas:
			aux=[school.ident, school.paraderos[0].stop_id, school.cantidad_salas]
			self.school.append(aux)
		for school in self.escuelas:
			for busstop in school.paraderos:
				for fakebusstop in busstop.fakebusstops:
					aux=[fakebusstop.fake_bus_stop_id, fakebusstop.bus_stop_id, fakebusstop.grade, fakebusstop.students]
					self.fakebusstop.append(aux)


		for school in self.escuelas:
			shifts=[]
			for i in range(0, school.turnos):
				shifts.append([])
				if school.multiseriada:
					shifts[i].append(0)
					shifts[i].append(0)
				else:
					for u in range(0, 11):
						shifts[i].append(0)
			for busstop in school.paraderos:
				for fakebusstop in busstop.fakebusstops:
					if school.multiseriada:
						if(fakebusstop.grade<3):
							shifts[fakebusstop.shift-1][0]=shifts[fakebusstop.shift-1][0]+fakebusstop.students
						else:
							shifts[fakebusstop.shift-1][1]=shifts[fakebusstop.shift-1][1]+fakebusstop.students
					else:
						shifts[fakebusstop.shift-1][fakebusstop.grade-1]=shifts[fakebusstop.shift-1][fakebusstop.grade-1]+fakebusstop.students
			u=0
			#print(school.cantidad_real)
			#raw_input()
			for shift in shifts:
				u=u+1
				j=0
				for grade in shift:
					j=j+1
					self.sol_shift_programming.append([school.ident,u,j,int(math.ceil(float(float(grade)/float(school.cantidad_real))))])





	def Sol_fakebusstop_shifts(self):
		for school in self.escuelas:
			#if school.turnos==1:
			#	for busstop in school.paraderos:
			#		for fakebusstop in busstop.fakebusstops:
			#			fakebusstop.shift=1
			#	school.cantidad_real=school.cantidad_alumnos
			#else:
				capacities=[]
				if school.multiseriada:
					students_in_grade=[]
					i=0
					while i< 2:
						students_in_grade.append(0)
						i=i+1
					for busstop in school.paraderos:
					#	print busstop.bus_stop_id
					#	raw_input()
						for fakebusstop in busstop.fakebusstops:
							if fakebusstop.grade<3:
								students_in_grade[0]=students_in_grade[0]+fakebusstop.students
							else:
								students_in_grade[1]=students_in_grade[1]+fakebusstop.students
					#for grade in students_in_grade:
					#	print grade
					#	raw_input()
					rooms=[]
					room_capacity=school.cantidad_alumnos
					for shift in range(0, school.turnos):
						rooms.append(school.cantidad_salas)
					rooms_per_grade0=[]
					rooms_per_grade1=[]
					total_rooms=school.turnos*school.cantidad_salas+1
					firsttime=0
					while total_rooms>school.cantidad_salas*school.turnos:
						total_rooms=0
						if firsttime==1:
							room_capacity=room_capacity+1
						else:
							firsttime=1
						for j in range(0, len(students_in_grade)):
							aux= math.ceil(float(float(students_in_grade[j])/float(room_capacity)))
							total_rooms=total_rooms+aux	
					rooms_available=school.turnos*school.cantidad_salas
					#print(students_in_grade[0])
					rooms_needed_grade0= math.ceil(float(float(students_in_grade[0])/float(room_capacity)))
					int(rooms_needed_grade0)
					#print(rooms_needed_grade0)
					#raw_input()
					rooms_needed_grade1= math.ceil(float(float(students_in_grade[1])/float(room_capacity)))
					int(rooms_needed_grade1)
					#print (school.cantidad_real)
					school.cantidad_real=room_capacity
					#print (school.cantidad_real)
					#raw_input()
					for sala in range(1, rooms_available+1):
						if sala<=rooms_needed_grade0:
							if sala<=school.cantidad_salas:
								rooms_per_grade0.append([room_capacity, 1])
							elif sala> school.cantidad_salas and sala<=school.cantidad_salas*2:
								rooms_per_grade0.append([room_capacity, 2])
							else:
								rooms_per_grade0.append([room_capacity, 3])
						else:
							if sala<=school.cantidad_salas:
								rooms_per_grade1.append([room_capacity, 1])
							elif sala> school.cantidad_salas and sala<=school.cantidad_salas*2:
								rooms_per_grade1.append([room_capacity, 2])
							else:
								rooms_per_grade1.append([room_capacity, 3])

					for busstop in school.paraderos:
						for fakebusstop in busstop.fakebusstops:
							if fakebusstop.grade<3:
					#			print "entre"
					#			print (rooms_per_grade0)
					#			raw_input()

								for sala in rooms_per_grade0:
					#				print sala[0]
					#				print fakebusstop.students
									if sala[0]>=fakebusstop.students:
										sala[0]=sala[0]-fakebusstop.students
										fakebusstop.shift=sala[1]
										break
					#				print sala[0]
					#				print fakebusstop.shift
					#				raw_input()

							else:
								for sala in rooms_per_grade1:
									if sala[0]>=fakebusstop.students:
										sala[0]=sala[0]-fakebusstop.students
										fakebusstop.shift=sala[1]
										break
					#for shift in range(0, school.turnos)						
					#	capacity=[]		
					#	for classroom in range(0, school.cantidad_salas):
					#		capacity.append(school.cantidad_alumnos/(school.cantidad_salas*school.turnos))
					#	capacities.append(capacity)							
					#for busstop in school.paraderos:	
					#	for fakebusstop in busstop.fakebusstops:
					#		j=0							
					#		for capacity in capacities:	
					#			i=0
					#			j=j+1
					#			while i<len(capacity):
					#				if fakebusstop.students<=capacity[i]:
					#					fakebusstop.shift=j
					#					capacity[i]=capacity[i]-fakebusstop.students
					#					break
					#				i=i+1
					#			if fakebusstop.shift==j:
					#				break
				else:
					students_in_grade=[]
					i=0
					while i< school.cantidad_cursos:
						students_in_grade.append(0)
						i=i+1
					for busstop in school.paraderos:
						for fakebusstop in busstop.fakebusstops:
							students_in_grade[fakebusstop.grade-1]=students_in_grade[fakebusstop.grade-1]+fakebusstop.students
					rooms=[]
					room_capacity= school.cantidad_alumnos
					for shift in range(0, school.turnos):
						rooms.append(school.cantidad_salas)
					rooms_per_grade=[]
					total_rooms=school.turnos*school.cantidad_salas+1
					firsttime=0
					while total_rooms>school.cantidad_salas*school.turnos:
						total_rooms=0
						if firsttime==1:
							room_capacity=room_capacity+1

						else:
							firsttime=1
						aux1000=0
						for j in range(0, len(students_in_grade)):
							aux= math.ceil(float(float(students_in_grade[j])/float(room_capacity)))
							aux1000=aux1000+students_in_grade[j]
							total_rooms=total_rooms+aux	
					#print (school.cantidad_real)
					school.cantidad_real=room_capacity
					#print (school.cantidad_real)
					#raw_input()

					for j in range(0, len(students_in_grade)):
						aux= math.ceil(float(float(students_in_grade[j])/float(room_capacity)))
						rooms_per_grade.append(aux)
					rooms_leftshift=[]
					for roomleft in range(0, school.turnos):
						rooms_leftshift.append(school.cantidad_salas)

					for roomleft in rooms_leftshift:
						actualgrade=0
						for room in rooms_per_grade:
							i=1
							actualgrade=actualgrade+1
							for roomsleft in range(0, len(rooms_leftshift)):
								if room <= rooms_leftshift[roomsleft]:
									rooms_leftshift[roomsleft]=rooms_leftshift[roomsleft]-room
									for busstop in school.paraderos:
										for fakebusstop in busstop.fakebusstops:
											if fakebusstop.grade==actualgrade:
												fakebusstop.shift=i
									break
								else:
									i=i+1								
					failed=False
					for busstop in school.paraderos:
						for fakebusstop in busstop.fakebusstops:
							if fakebusstop.shift==0:
								failed=True

					if failed:
						while True:
							aux=0
							for busstop in school.paraderos:
								for fakebusstop in busstop.fakebusstops:
									if fakebusstop.shift==0:
										aux=fakebusstop.grade
										break
								if aux>0:
									break
							if aux>0:	
								room=rooms_per_grade[aux-1]
								i=0
								students_per_room=int(students_in_grade[aux-1]/room)+1
								for rooms_left in rooms_leftshift:
									i=i+1
									if rooms_left>0:
										if room> rooms_left:
											partial_students= rooms_left*students_per_room
											room=room-rooms_left
											rooms_left=0
											for busstop in school.paraderos:
												for fakebusstop in busstop.fakebusstops:
													if fakebusstop.grade==aux and fakebusstop.shift==0:
														if fakebusstop.students<=partial_students:
															partial_students=partial_students-fakebusstop.students
															fakebusstop.shift=i
											if partial_students>0:
												aux1=0
												aux2=0
												aux3=0
												for busstop in school.paraderos:
													for fakebusstop in busstop.fakebusstops:
														if fakebusstop.grade==aux and fakebusstop.shift==0:
															if aux1==0:
																aux1=fakebusstop.fake_bus_stop_id
																aux2=fakebusstop.students
																aux3=busstop.bus_stop_id
															elif fakebusstop.students<aux2:
																aux1=fakebusstop.fake_bus_stop_id
																aux2=fakebusstop.students
																aux3=busstop.bus_stop_id
												if aux2>0:
													for busstop in school.paraderos:
														for fakebusstop in busstop.fakebusstops:
															if fakebusstop.fake_bus_stop_id==aux1:
																fakebusstop.shift=i
										elif room<=rooms_left:
											rooms_left=rooms_left-room
											for busstop in school.paraderos:
													for fakebusstop in busstop.fakebusstops:
														if fakebusstop.grade==aux and fakebusstop.shift==0:
															fakebusstop.shift=i
															partial_students=0



							else:
								break

		for school in self.escuelas:
			for busstop in school.paraderos:
				for fakebusstop in busstop.fakebusstops:
					self.sol_fakebusstop_shifts.append([fakebusstop.fake_bus_stop_id , fakebusstop.school_id, fakebusstop.bus_stop_id, fakebusstop.shift])
	

	def Asign_Routes(self):
		for school in self.escuelas:
			for shift in range(1, school.turnos+1):
				for busstop in school.paraderos:
						busstop.inroute=False
				for busstop in school.paraderos:
					if busstop.ubicacionx==school.ubicacionx and busstop.ubicaciony==school.ubicaciony:
						school.Set_stop_id(busstop.stop_id)
						school.bus_stop_id=busstop.bus_stop_id
						busstop.inroute=True
						break				
				u=1
				while True:
					route=[]
					route.append([school.ident, shift, u, 0, 0])
					stop1=school.stop_id
					stop1ubicx=school.ubicacionx
					stop1ubicy=school.ubicaciony
					stop2=0
					stop2ubicx=0
					stop2ubicy=0
					distance=0
					capacityleft=self.buscapacity
					i=1
					while True:
						for busstop in school.paraderos:
							distanceaux=math.sqrt(math.pow(stop1ubicx-busstop.ubicacionx,2)+math.pow(stop1ubicy-busstop.ubicaciony,2))
							if stop1==school.stop_id and distanceaux>distance and busstop.inroute==False:
								fakeinshift=False
								for fakebusstop in busstop.fakebusstops:
									if fakebusstop.inroute==False and fakebusstop.shift==shift and fakebusstop.students<=capacityleft:
										fakeinshift=True
										break
								if fakeinshift:
									distance=distanceaux
									stop2=busstop.bus_stop_id
									stop2ubicx=busstop.ubicacionx
									stop2ubicy=busstop.ubicaciony
							elif stop1!=busstop.stop_id and distanceaux<distance and busstop.inroute==False:
								fakeinshift=False
								for fakebusstop in busstop.fakebusstops:
									if fakebusstop.inroute==False and fakebusstop.shift==shift and fakebusstop.students<=capacityleft:
										fakeinshift=True
										break
								if fakeinshift:
									distance=distanceaux
									stop2=busstop.bus_stop_id
									stop2ubicx=busstop.ubicacionx
									stop2ubicy=busstop.ubicaciony
							elif stop1!=busstop.stop_id and distance==0 and busstop.inroute==False:
								fakeinshift=False
								for fakebusstop in busstop.fakebusstops:
									if fakebusstop.inroute==False and fakebusstop.shift==shift and fakebusstop.students<=capacityleft:
										fakeinshift=True
										break
								if fakeinshift:
									distance=distanceaux
									stop2=busstop.bus_stop_id
									stop2ubicx=busstop.ubicacionx
									stop2ubicy=busstop.ubicaciony
						
						for busstop in school.paraderos:
							if stop2==busstop.bus_stop_id:
								busstop.inroute=True
								for fakebusstop in busstop.fakebusstops:
									if fakebusstop.shift==shift and fakebusstop.students<=capacityleft and fakebusstop.inroute==False:
										capacityleft = capacityleft-fakebusstop.students
										fakebusstop.inroute=True
										route.append([school.ident, shift, u, fakebusstop.fake_bus_stop_id, i])
										i=i+1
									elif fakebusstop.shift==shift and fakebusstop.inroute==False and fakebusstop.students>capacityleft:
										busstop.inroute=False
								stop1=stop2
								stop1ubicx=stop2ubicx
								stop1ubicy=stop2ubicy
								break

						if stop2==0 or capacityleft==0:
							break
						stop2=0
						stop2ubicx=0
						stop2ubicy=0
						distance=100000
					for stop in route:
						self.routes.append(stop)
					u=u+1
					reverse=len(route)
					for mirror in range(0,len(route)):
						if mirror==0:
							things=[]
							for thing in route[0]:
								things.append(thing)
							self.routes.append([things[0], things[1], u, things[3], things[4]])
						else:
							things=[]
							for thing in route[mirror]:
								things.append(thing)
							self.routes.append([things[0], things[1], u, things[3], reverse])
						reverse=reverse-1

					finish=False
					for busstop in school.paraderos:
						if busstop.stop_id != school.stop_id:
							for fakebusstop in busstop.fakebusstops:
								if fakebusstop.shift==shift and fakebusstop.inroute==False:
									finish=True
									break
						if finish:
							break					
					if finish==False:
						break
					u=u+1

def read_table(ruta_archivo):
	archivo = open(str(ruta_archivo))
	datos = archivo.read()
	archivo.close()
	datos_linea = datos.split('\n')
	arreglo = []
	for i in datos_linea:
		arreglo.append(i.split('\t'))
	return arreglo

def write_table(file_route, table):
	f = open(str(file_route),"w")
	for item in table:
		f.write(str(item)+"\n")
	f.close()


if __name__ == "__main__":
	## codigo de main	
	aux= str()
	aux=raw_input("Escriba el directorio del archivo de entrada: ")
	complete=read_table(aux)
	schooldata=[]
	size=[]
	schooltype=[]
	center=[]
	#center[centrox, centroy, radio]
	buscapacity=0
	i=0
	maxfake=0
	for line in complete:

		if i==0:
			size.append(int(line[0]))
			size.append(int(line[1]))
		elif i==1:
			center.append(int(line[0]))
			center.append(int(line[1]))
		elif i==2:
			center.append(int(line[0]))
		elif i==3:
			buscapacity=int(line[0])
		elif i==4:
			maxfake=int(line[0])			
		else:
			if line[1]=='m' and line[2]=='u': 
				schooltype.append([int(line[0]),True,0,int(line[3]), int(line[4]),int(line[5])])
			elif line[1]=='s' and line[2]=='u': 
				schooltype.append([int(line[0]),False,0,int(line[3]), int(line[4]),int(line[5])])
			elif line[1]=='m' and line[2]=='r': 
				schooltype.append([int(line[0]),True,1,int(line[3]), int(line[4]),int(line[5])])
			elif line[1]=='s' and line[2]=='r': 
				schooltype.append([int(line[0]),False,1,int(line[3]), int(line[4]),int(line[5])])			
			elif line[1]=='m' and line[2]=='f':
				schooltype.append([int(line[0]),True,2,int(line[3]), int(line[4]),int(line[5])])
			elif line[1]=='s' and line[2]=='f':
				schooltype.append([int(line[0]),False,2,int(line[3]), int(line[4]),int(line[5])])
			else:
				for typeschool in schooltype:
					if typeschool[0]== int(line[0]):
						if typeschool[2]==2:
							schooldata.append([int(line[0]),float(line[1]),float(line[2]),float(line[3]), float(line[4]), float(line[5]), float(line[6])])	
						else:	
							schooldata.append([int(line[0]),float(line[1]),float(line[2]),float(line[3]),0,0, float(line[4])])
						break

		i=i+1

	county=Municipalidad(buscapacity)
	schooldata2=[]
	for school in schooldata:
		schooldata2.append([school[2], school[1], schooltype[school[0]-1][1], schooltype[school[0]-1][2], schooltype[school[0]-1][3], schooltype[school[0]-1][4], schooltype[school[0]-1][5], school[3], school[4], school[5], school[6]])
	county.crearescuelas(schooldata2, center[0], center[1], center[2], size[0], size[1], maxfake)
	county.Sol_fakebusstop_shifts()
	county.Asign_Routes()
	county.tables()

	writer= raw_input("Escriba la ruta de los archivos de salida: ")
	aux= writer
	writer=aux+"stop.txt"
	write_table(writer, county.stop)
	writer=aux+"distance.txt"
	write_table(writer, county.distance)
	writer=aux+"busstop.txt"
	write_table(writer, county.busstop)
	writer=aux+"grade_busstop.txt"
	write_table(writer, county.grade_busstop)
	writer=aux+"school.txt"
	write_table(writer, county.school)
	writer=aux+"fakebusstop.txt"
	write_table(writer, county.fakebusstop)
	writer=aux+"routes.txt"
	write_table(writer, county.routes)
	writer=aux+"sol_fakebusstop_shifts.txt"
	write_table(writer, county.sol_fakebusstop_shifts)
	writer=aux+"sol_shift_programming.txt"
	write_table(writer, county.sol_shift_programming)