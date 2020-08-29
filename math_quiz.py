import os

os.environ["NO_KIVY_LOG"] = "1"

from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock

from kivy.core.window import Window
from kivy.uix.button import Label,Button
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout

import time, random, queue, sqlite3

Builder.load_string("""
#:import c_hex kivy.utils.get_color_from_hex
#:import wb webbrowser

#:set font_name 'monaco.ttf'
#:set size 16
#:set c_red 'FF0B00'
#:set c_green '00FF21'
#:set c_canvas '3B002C'

<Button>:
	font_size:dp(size)
	font_name:font_name
	size_hint_y:.2

<MyButton>:
	
	background_normal:''
	background_color:[0,0,0,0]
	canvas.before:
		Color:
			rgb: c_hex(c_canvas)
		Rectangle:
			size:self.size
			pos:self.pos

<TextInput>:
	font_size:dp(size)
	font_name:font_name
	multiline:False

<Label>:
	font_name:font_name
	font_size:dp(size)

<MenuNya>:
	orientation:'vertical'
	padding:20
	Label:
		text:'Simple Math Kuis [color={0}](19-10)×18[/color]'.format(c_red)
		markup:True
		
	BoxLayout:
		spacing:15
		orientation:'vertical'
		size_hint_y:.5
		Button:
			text:'Hard'
			on_release:app.root.soall(self.text)
		Button:
			text:'Easy'
			on_release:app.root.soall(self.text)
		Button:
			text:'History'
			id:history
			on_release:app.root.history()
			
	Button:
		size_hint_y:.6
		text:'dev: [u][color={0}]Muhammad Ikbal[/color][/u]'.format(c_green)
		markup:True
		background_color:[0,0,0,0]
		background_normal:''
		background_down:''
		on_release:
			wb.open('https://mbasic.facebook.com/Xiuz.Maoundis')

<BaseApk>:
	orientation:'vertical'

		
<SoalNya>:
	BoxLayout:
		orientation:'vertical'
		padding:20
		Label:
			size_hint_y:.4
			id:adalah
			
		BoxLayout:
			size_hint_y:.5
			ProgressBar:
				id:progress
				size_hint_x:.7
			Label:
				id:waktu
				size_hint_x:.3
		
		Label:
			size_hint_y:.9
			id:soalnya
			canvas.before:
				Color:
					rgb:c_hex(c_canvas)
				Rectangle:
					size:self.size
					pos:self.pos
			

		Label:
			size_hint_y:.2
			font_size:dp(size - 3)
			id:pesan
			
		BoxLayout:
			padding:10
			
			size_hint:[.4,.2]
			canvas.before:
				Color:
					rgb:c_hex(c_canvas)
				Rectangle:
					pos:self.pos
					size:self.size
			Label:
				text:'skormu:'
				size_hint_x:.1
				
			Label:
				id:skormu
				text:'0'
				size_hint_x:.1
				color: c_hex(c_red if self.text == '0' else c_green)
				


		BoxLayout:
			size_hint_y:1
			TextInput:
				id:jawaban
				font_size:dp(size + 15)
				size_hint_x:.7
				size_hint_y:.3
				cursor_width:3
				
				
			Button:
				size_hint_x:.3
				size_hint_y:.3
				text:'Jawab'
				on_release:
					root.jawab(jawaban.text)
				
		Button:
			text:'stop'
			size_hint_y:.4
			font_size:dp(size + 10)
			on_release:
				root.klok_stop()
				app.root.hasil([skormu.text, root.waktumu, root.list_soal])

		Label:
			size_hint_y:.7
			
<ShowHistory>:
	orientation:'vertical'
	spacing:40
	padding:20
	Label:
		id:total
		size_hint_y:.1
		
		canvas.before:
			Color:
				rgb:(.1,0,.1)
			Rectangle:
				pos:[170,870]
				size:200,50
	
	BoxLayout:
		orientation:'vertical'
		size_hint_y:.8
		ScrollView:
			BoxLayout:
				orientation:'vertical'
				spacing:10
				size_hint_y:None
				height:self.minimum_height
				id:historyku
		
	Button:
		size_hint_y:.1
		text:'Back'
		on_release:app.root.menuy()
			
			
<HasilMu>:
	orientation:'vertical'
	spacing:40
	padding:20
	BoxLayout:
		orientation:'vertical'
		spacing:5
		size_hint_y:.3
		
		canvas.before:
			Color:
				rgb:c_hex(c_canvas)
			Rectangle:
				size:self.size
				pos:self.pos			
		Label:
			id:skormuh
		
		Label:
			id:waktumu
		
		Label:
			id:tipe


	ScrollView:
		BoxLayout:
			orientation:'vertical'
			size_hint_y:None
			height:self.minimum_height
			id:show_hasil

	Button:
		size_hint_y:.1
		text:'Main Lagi?'
		on_release:app.root.menuy()

""")

class MyButton(Button):
	def __init__(self,**kwargs):
		super(MyButton,self).__init__(**kwargs)

class DataBase:
	def __init__(self):
		self.db = sqlite3.connect('data.db')

	def get_jumlah(self):
		try:
			id = len(list(self.db.execute('select id from list_hitory')))
		except:
			id = 0
			self.db.execute('create table list_hitory(id int primary key, skormu int, waktu text, tipe text, tanggal text)')
		finally:
			self.db.commit()
			return id

	def get_value(self):
		
		value = self.db.execute('select * from list_hitory')
		self.db.commit()
		for x in value:
			yield x
			
	
	def add_data(self, value):
		self.db.execute('insert into list_hitory(id, skormu, waktu, tipe, tanggal) values(?,?,?,?,?)',value)
		self.db.commit()
		
	def delet_data(self, id):
		self.db.execute('delete from list_hitory where id=%d' % id)
		self.db.commit()
	
	def _close(self):
		self.db.close()
		
class ShowHistory(BoxLayout):
	def __init__(self, **kwargs):
		super(ShowHistory, self).__init__(**kwargs)
		
		self.refresh()
	
	def refresh(self):
		self.db = DataBase()
		self.dt = self.db.get_value()
		
		if hasattr(self,'kok'):
			self.kok.cancel()
		self.ids.total.text = 'total: ' + str(self.db.get_jumlah())
		self.ids.historyku.clear_widgets()
		
		self.kok = Clock.schedule_interval(self.memsk,0.01)
		
	def memsk(self,*i):
		try:
			data = next(self.dt)
			id = data[0]
			skor = 'skor: ' + str(data[1])
			waktu = data[2]
			tipe = 'tipe: ' + data[3]
			tanggal = 'tanggal: ' + data[4]
			bx = BoxLayout(orientation='vertical', size_hint_y=None,height=200)
			
			bx.add_widget(MyButton(size_hint_y=.5,
						text=skor))
			bx.add_widget(MyButton(size_hint_y=.5,
						text=waktu))
			bx.add_widget(MyButton(size_hint_y=.5,
						text=tipe))
			bx.add_widget(MyButton(size_hint_y=.5,
						text=tanggal))
						
			btn = Button(text='Hapus',size_hint_y=.5)

			btn.bind(on_release=lambda x:self.delete_item(id))
			bx.add_widget(btn)
			self.ids.historyku.add_widget(bx)
			
		except:
			self.kok.cancel()
			
	def delete_item(self,id):
		self.db.delet_data(id)
		self.db._close()
		self.refresh()
		
	
class HasilMu(BoxLayout):
	def __init__(self, data,**kwargs):
		super(HasilMu, self).__init__(**kwargs)
		
		self.skor = data[0]
		self.waktu = data[1]
		self.soal = data[2][1]
		self.tipe = data[2][0]
	
		Clock.schedule_once(self.yoaihk,0.001)
		Clock.schedule_interval(self.show_yes,0.001)
		Clock.schedule_once(self.show_popup,0.000001)
	
	
	def simpan_ke_db(self):
		
		self.popup.dismiss()
		
		db = DataBase()
		id = db.get_jumlah() + 1
		db.add_data((id, self.skor, self.ids.waktumu.text, self.tipe, time.ctime()))
		db._close()
		
		
		
	
	def show_popup(self, *i):
		bx=BoxLayout(orientation='vertical')
		btn=Button(text='Simpan')
		
		btn1=Button(text='Tidak')
		bx.add_widget(btn)
		bx.add_widget(btn1)
		self.popup = Popup(
			title='pesan: ',
			content=bx,
			size_hint=[.4,.2],
			auto_dismiss=False
		)
		self.popup.open()
		btn.bind(on_release=lambda x:self.simpan_ke_db())
		btn1.bind(on_release=lambda x:self.popup.dismiss())
	
	def show_yes(self, *i):
		try:
			if self.soal.qsize():
				
				data=self.soal.get()
				
				bx = BoxLayout(size_hint_y=None,height=100)
				bx.add_widget(MyButton(size_hint_y=.4,
						text=data[0],size_hint_x=.4))
				bx.add_widget(MyButton(size_hint_y=.4,
						text=data[1],size_hint_x=.2))
				
				bx.add_widget(MyButton(size_hint_y=.4,
						markup=True,text=data[2],size_hint_x=.3))
				
				btn = MyButton(text='×',size_hint_x=.1,size_hint_y=.4)
				btn.bind(on_release=lambda x:self.ids.show_hasil.remove_widget(bx))
				bx.add_widget(btn)
				self.ids.show_hasil.add_widget(bx)
			
			
		except:
			
			Clock.unschedule(self.show_yes)
	
	
	def yoaihk(self, *i):
		waktu = '{0} detik'.format(self.waktu)
		if self.waktu > 60:
			waktu = '{0} menit'.format(self.waktu // 60)
		
		self.ids.skormuh.text = 'skor: {0}'.format(self.skor)
		self.ids.waktumu.text = 'waktu: {0}'.format(waktu)
		self.ids.tipe.text = 'type: {0}'.format(self.tipe.title())
		
class MenuNya(BoxLayout):
	def __init__(self,**kwargs):
		super(MenuNya, self).__init__(**kwargs)
		Db = DataBase()
		j_dt = Db.get_jumlah()
		Db._close()
		self.ids.history.disabled = True if not j_dt else False
		
		
class SoalNya(BoxLayout):
	def __init__(self,tipe, **kwargs):
		super(SoalNya, self).__init__(**kwargs)

		self.c_red = 'FF0B00'
		self.c_green = '00FF21'
		
		
		self.stops = 10
		self.jeda_pesan = 4

		self.angka_pertama = lambda: random.randint(15,150)
		self.angka_terakhir = lambda: random.randint(15,300)
			
		
		if tipe == 'easy':
			self.stops = 20
			
			self.angka_pertama = lambda: random.randint(10,70)
			self.angka_terakhir = lambda: random.randint(10,150)


		self.ids.progress.max = self.stops
		self.mulai = self.stops
		Clock.schedule_interval(self.waktunya, 0.9)
		self.waktumu = 0
		self.list_soal = [tipe, queue.Queue()]

	def waktunya(self, *i):
		self.waktumu += 1
		
		if not self.jeda_pesan:
			self.ids.adalah.text = ''
			self.ids.pesan.text = ''
			self.jeda_pesan = 4
		
		if self.ids.pesan.text or self.ids.adalah.text:
			self.jeda_pesan -= 1
		
		
		if self.mulai >= self.stops:
			if hasattr(self,'jawaban'):
				if not 'Bro' in self.ids.adalah.text and len(str(self.jawaban)) <= 8:
					jwbn = str(self.jawaban)
					self.ids.adalah.text = 'jawabannya adalah: ({0})'.format(jwbn if len(jwbn) < 7 else '\n' + jwbn)
					
			
			tipe_math = random.choice([
			
				['+','penjumlahan'],
				['*','perkalian'],
				['-','pengurangan'],
				['/','pembagian']
				
			])
			self.soaltz = '{0} {1} {2}'.format(self.angka_pertama(),tipe_math[0],self.angka_terakhir())
			self.jawaban = abs(eval(self.soaltz))
			
			if len(str(self.jawaban)) >= 8:
				self.mulai = self.stops - 1
			else:
				self.soaltz = self.soaltz.replace('/','÷').replace('*','×')
				
				self.ids.soalnya.text = '\n\nBerapa hasil \ndari {0} di bawah ini:  \n\n {1} = {2} \n'.format(tipe_math[1], self.soaltz, '?' * len(str(self.jawaban))) 
				self.mulai = 0
			
			
		self.mulai += 1
		self.ids.progress.value = self.mulai
		self.ids.waktu.text = '{0} / {1}'.format(self.mulai, self.stops)
	
	
	def jawab(self, jawaban):
		def g(*i):
			if jawaban.isdigit():
				
				
				
				if int(jawaban) == self.jawaban:
					
					
					self.list_soal[1].put([self.soaltz, jawaban, '[color={0}]{1}[/color]'.format(self.c_green , 'Benar')])
				
					self.ids.pesan.text = 'Benar Bro =)'
					self.ids.skormu.text = str(int(self.ids.skormu.text) + 1)
				else:
					self.list_soal[1].put([self.soaltz, jawaban, '[color={0}]{1}[/color]'.format(self.c_red , 'Salah')])
				
					self.ids.skormu.text = str(int(self.ids.skormu.text) - 1) if int(self.ids.skormu.text) > 0 else '0'
					self.ids.pesan.text = 'jawaban salah ×'
					
				self.mulai = self.stops
			else:
				
				self.ids.pesan.text = 'harus angka asu'
			self.ids.jawaban.text = ''
			
		Clock.schedule_once(g,0.1)
	def klok_stop(self):
		Clock.unschedule(self.waktunya)


class BaseApk(BoxLayout):
	def __init__(self, **kwargs):
		super(BaseApk, self).__init__(**kwargs)
		Clock.schedule_once(self.menuy,0.000001)


	def menuy(self,*i):
		self.clear_widgets()
		self.menunya = MenuNya()
		self.add_widget(self.menunya)
	

	def soall(self, tipe):
		self.menunya = SoalNya(tipe.lower())
		self.clear_widgets()
		self.add_widget(self.menunya)
		
		
	def hasil(self, hasil):
		self.menunya = HasilMu(hasil)
		self.clear_widgets()
		Clock.schedule_once(lambda x:self.add_widget(self.menunya),0.1)
	
	def history(self):
		self.menunya = ShowHistory()
		self.clear_widgets()
		Clock.schedule_once(lambda x:self.add_widget(self.menunya),0.1)
	

class MainBuild(App):
	Window.softinput_mode = 'below_target'
	def on_create(self):
		if os.path.exists('.kivy'):
			os.system('rm -rf .kivy/logs')
		
	def build(self):
		return BaseApk()

if __name__=='__main__':
	MainBuild().run()