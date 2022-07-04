import tkinter as tk
from tkinter import simpledialog,messagebox
from PIL import Image,ImageTk
import numpy as np
import time
from hormiga import createAnts,createBoard,takeStep

class mainWindow():
	def __init__(self):
		# prev_step = -1 --> update canvas
		self.prev_step = 0
		self.step = 0
		self.fps = 100
		self.delta_t = 1/self.fps
		self.playing = False
		self.rows = 200
		self.columns = 200
		self.ant = "LR"
		self.ant_color = (255,0,0) # Red
		self.hormigas_iniciales = createAnts(1,self.rows,self.columns)
		# Colors = [black,white,blue,green,purple,teal,darkgreen,greeny-blue,pink,orange,lemon,yellow,gold]
		self.colors = [(0,0,0),(255,255,255),(0,0,255),(0,255,0),(128,0,255),(0,255,255),(0,64,0),(0,255,128),(255,0,128),(255,128,0),(128,255,0),(255,255,0),(128,128,0)]
		self.game_start()
		# Interface
		self.root = tk.Tk()
		self.root.title("Hormiga de Langton")
		self.root.bind("<Configure>",self.cambio_de_tamano)
		self.recuadro = tk.Frame(self.root, width=600, height=500)
		self.recuadro.pack()
		self.canvas = tk.Canvas(self.recuadro, width=500,height=400)
		self.fpsString = tk.StringVar()
		self.stepString = tk.StringVar()
		self.langtonString = tk.StringVar()
		self.boardString = tk.StringVar()
		self.antsString = tk.StringVar()
		self.labelFPS = tk.Label(self.recuadro,textvariable=self.fpsString)
		self.labelStep = tk.Label(self.recuadro,textvariable=self.stepString)
		self.labelLangton = tk.Label(self.recuadro,textvariable=self.langtonString)
		self.fpsString.set("FPS: "+str(self.fps))
		self.stepString.set("Step actual: 0")
		self.langtonString.set("Hormiga de Langton: "+self.ant)
		self.boardString.set("Tablero: filas="+str(self.rows)+", cols="+str(self.columns))
		self.boton_de_play = tk.Button(self.recuadro, text="Play",command=self.estripar_play,bg="green")
		self.boton_hormigas = tk.Button(self.recuadro, text="Tablero",command=self.estripar_modificar,bg="firebrick1")
		self.boton_patron = tk.Button(self.recuadro, text="Patrón",command=self.cambio_de_patron_hormigas,bg="medium purple")
		self.boton_reset = tk.Button(self.recuadro, text="Reset",command=self.estripar_reset, bg="indian red")
		self.antsChooser = None
		# Show ants
		self.visibleInt = tk.IntVar()
		self.visibleInt.set(1)
		# Start
		self.root.after(0,self.update_loop)
		self.root.mainloop()
		
	def game_start(self):
		self.ants = []
		for ant in self.hormigas_iniciales:
			self.ants.append(ant.copy())
		self.board = createBoard(self.rows,self.columns)

	def cambio_de_tamano(self,event):
		if event.widget == self.root:
			center_offset = (event.width - 600)/2 if event.width>600 else 0
			self.canvas_width = event.width - 100
			self.canvas_height = event.height - 100
			self.recuadro.configure(width=event.width,height=event.height)
			self.canvas.configure(width=self.canvas_width,height=self.canvas_height)
			self.canvas.place(x=50,y=20)
			self.labelFPS.place(x=center_offset+10,y=self.canvas_height+40)
			self.labelStep.place(x=center_offset+10,y=self.canvas_height+60)
			self.labelLangton.place(x=center_offset+320, y=self.canvas_height+30)
			self.boton_de_play.place(x=center_offset+280, y=self.canvas_height+55)
			self.boton_hormigas.place(x=center_offset+320, y=self.canvas_height+55)
			self.boton_patron.place(x=center_offset+410, y=self.canvas_height+55)
			self.boton_reset.place(x=center_offset+470, y=self.canvas_height+40,height=50,width=70)
			self.prev_step = -1

	def update_loop(self):
		if self.playing:
			self.current_time = time.time()
			for i in range(0,int((self.current_time - self.previous_time)*self.fps)):
				self.game_step()
			self.previous_time = self.current_time - (self.current_time - self.previous_time)%self.delta_t
		if self.prev_step < self.step:
			self.resize_cuadro()
		self.root.after(int(1000/10),self.update_loop)

	def resize_cuadro(self):
		self.stepString.set("Current step: "+str(self.step))
		self.prev_step = self.step
		pixels = np.array( [[self.colors[int(y)] for y in x] for x in self.board] )
		if self.visibleInt.get()>0:
			for ant in self.ants:
				pixels[ant[0]%self.rows][ant[1]%self.columns] = self.ant_color
		self.image = Image.fromarray(pixels.astype('uint8'), 'RGB')
		self.photo = ImageTk.PhotoImage(image=self.image.resize((self.canvas_width,self.canvas_height)))
		self.canvas.create_image(0,0,image=self.photo,anchor=tk.NW)

	def estripar_play(self):
		self.previous_time = time.time()
		self.playing = not self.playing
		self.boton_de_play.configure(text="Stop" if self.playing else "Play",bg="red" if self.playing else "green")

	def cambio_de_patron_hormigas(self):
		nuevo_valor = simpledialog.askstring("Hormiga de Langton","Elija el nuevo patrón:", parent=self.recuadro)
		if nuevo_valor is None:
			return
		nuevo_valor = nuevo_valor.upper()
		if nuevo_valor == self.ant or len(nuevo_valor)==0:
			return
		for c in nuevo_valor:
			if c not in ['L','R','N','U']:
				messagebox.showerror("Entrada inválida", "Solo puede usar L,R,U,N.")
				return
		if len(nuevo_valor)>len(self.colors):
			messagebox.showwarning("Extensión máxima alcanzada","El máximo soportado es: "+str(len(self.colors))+"-char long sequences")
			nuevo_valor = nuevo_valor[0:len(self.colors)]
		self.ant = nuevo_valor
		self.langtonString.set("Hormigas de Langton: "+self.ant)
		self.estripar_reset()
	
	def estripar_reset(self):
		if self.playing:
			self.estripar_play()
		self.step=0
		self.prev_step = -1
		self.stepString.set("Step actual: "+str(self.step))
		self.game_start()
		
	def estripar_modificar(self):
		if self.antsChooser is None:
			self.antsChooser = tk.Toplevel(self.root, width = 250, height = 500)
			self.antsChooser.title("hormigas")
			self.antsChooser.protocol("WM_DELETE_WINDOW",self.antschooser_closing)
			labelBoard = tk.Label(self.antsChooser,textvariable=self.boardString)
			buttonBoard = tk.Button(self.antsChooser,command=self.tamano_presionar,text="Modificar",bg="sea green")
			labelBoard.place(x=10,y=15)
			buttonBoard.place(x=190,y=15)
			checkAnts = tk.Checkbutton(self.antsChooser,text="Hormigas visibles?",variable=self.visibleInt,command=self.resize_cuadro)
			checkAnts.place(x=150,y=50)
			self.antsString.set("Total de hormigas: "+str(len(self.ants)))
			labelAnts = tk.Label(self.antsChooser,textvariable=self.antsString)
			labelAnts.place(x=10,y=50)

	def antschooser_closing(self):
		self.antsChooser.destroy()
		self.antsChooser = None
	
	def tamano_presionar(self):
		nuevas_rows = simpledialog.askinteger("Nuevas filas", "Nuevo total de filas:",
                                parent=self.antsChooser,minvalue=1,initialvalue=self.rows)
		if nuevas_rows is not None:
			nuevas_cols = simpledialog.askinteger("Nuevas columnas", "Nuevo total de columnas:",
                                parent=self.antsChooser,minvalue=1,initialvalue=self.columns)
			if nuevas_cols is not None:
				self.rows = nuevas_rows
				self.columns = nuevas_cols
				self.boardString.set("Tablero: filas="+str(self.rows)+", cols="+str(self.columns))
				self.hormigas_iniciales = createAnts(len(self.ants),self.rows,self.columns)
				self.estripar_reset()
	
	def buttonnew_ants_press(self):
		self.hormigas_iniciales = createAnts(len(self.hormigas_iniciales),self.rows,self.columns)
		self.estripar_reset()
	
	def game_step(self):
		self.step+=1
		takeStep(self.board,self.ants,self.ant)

x = mainWindow()
