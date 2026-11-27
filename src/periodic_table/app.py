"""Flet presentation layer for PeriodicTable."""
import random
import flet as ft
from .repository import JsonElementRepository
from .services import ElementService, CompareService

BG="#F4F6F9"; BLUE="#315CEB"; TEXT="#202633"; MUTED="#667085"
COLORS={"No metal":"#DDF1E6","Gas noble":"#E9DDF6","Alcalino":"#F9E7C9","Alcalinotérreo":"#DCE8FA","Metaloide":"#F6DDE2","Halógeno":"#D7F0ED","Post-transición":"#EDE9CE","Transición":"#E5E8EF","Lantánido":"#F3DCEB","Actínido":"#F9E1D2"}

class PeriodicTableApp:
 def __init__(self,page:ft.Page):
  self.page=page; self.repo=JsonElementRepository(); self.service=ElementService(self.repo); self.compare=CompareService()
  self.favorites=set(); self.notes={}; self.collections={"Examen viernes":set(),"Metales":set(),"Gases":set()}
  self.selected=None; self.route="Tabla"; self.query=""; self.category="Todos"; self.search_category=None; self.search_block=None; self.search_period=None; self.quiz_mode="Símbolos"; self.quiz_index=0; self.score=0; self.streak=0; self.best=0; self.quiz_answer=None; self.quiz_checked=False; self.quiz_selected=None; self.settings={"Tema":"Claro","Idioma":"Español","Temperatura":"K","Tamaño":"Normal","Colores":True}
  page.title="PeriodicTable"; page.padding=0; page.bgcolor=BG; page.theme_mode=ft.ThemeMode.LIGHT; page.window_min_width=900; page.window_min_height=650
  self.root=ft.Row(spacing=0,expand=True,controls=[self.sidebar(),ft.Container(expand=True,padding=24,content=ft.Column(expand=True,scroll=ft.ScrollMode.AUTO,controls=[self.content()],spacing=18))])
  page.add(self.root)
 def text(self,s,size=14,weight=None,color=TEXT): return ft.Text(str(s),size=size,weight=weight,color=color)
 def btn(self,label,fn,primary=False): return ft.Button(label,on_click=fn,bgcolor=BLUE if primary else "#FFFFFF",color="white" if primary else TEXT)
 def card(self,content,padding=16): return ft.Container(content=content,bgcolor="white",border=ft.Border.all(1,"#E4E7EC"),border_radius=12,padding=padding)
 def sidebar(self):
  items=["Tabla","Buscar","Comparar","Quiz","Favoritos"]
  nav=[]
  for item in items:
   nav.append(ft.Container(content=ft.Text(item,weight=ft.FontWeight.W_600 if self.route==item else None,color=BLUE if self.route==item else TEXT),padding=12,border_radius=9,bgcolor="#E8EEFF" if self.route==item else None,on_click=lambda e,n=item:self.go(n)))
  nav.append(ft.Container(expand=True)); nav.append(ft.Container(content=self.text("Ajustes",color=BLUE if self.route=="Ajustes" else TEXT),padding=12,on_click=lambda e:self.go("Ajustes")))
  return ft.Container(width=150,bgcolor="white",border=ft.Border.only(right=ft.BorderSide(1,"#E4E7EC")),padding=12,content=ft.Column(controls=[ft.Text("PeriodicTable",size=18,weight=ft.FontWeight.BOLD),ft.Container(height=12),*nav],expand=True))
 def go(self,route): self.route=route; self.refresh()
 def refresh(self):
  self.root.controls[0]=self.sidebar(); self.root.controls[1].content.controls=[self.content()]; self.page.update()
 def header(self,title,subtitle): return ft.Column(spacing=2,controls=[self.text(title,25,ft.FontWeight.BOLD),self.text(subtitle,12,color=MUTED)])
 def content(self):
  return {"Tabla":self.table_view,"Buscar":self.search_view,"Comparar":self.compare_view,"Quiz":self.quiz_view,"Favoritos":self.favorites_view,"Ajustes":self.settings_view}.get(self.route,self.table_view)()
 def element_tile(self,e):
  bg=COLORS.get(e.category,"#E5E8EF") if self.settings["Colores"] else "#EEF1F5"
  dimensions={"Compacto":(54,62),"Normal":(64,72),"Grande":(74,82)}[self.settings["Tamaño"]]
  return ft.Container(width=dimensions[0],height=dimensions[1],bgcolor=bg,border_radius=7,padding=6,on_click=lambda ev,n=e.number:self.select(n),content=ft.Column(spacing=1,controls=[self.text(e.number,9,color=MUTED),self.text(e.symbol,19,ft.FontWeight.BOLD),self.text(e.name,8,color=MUTED)]))
 def table_view(self):
  elems=self.service.all(); cats=["Todos","Metales","No metales","Metaloides","Gases nobles","Favoritos"]
  tabs=ft.Row(wrap=True,controls=[self.btn(c,lambda ev,x=c:self.set_category(x),self.category==c) for c in cats])
  legend=ft.Row(wrap=True,spacing=10,controls=[ft.Row(spacing=4,controls=[ft.Container(width=10,height=10,bgcolor=c,border_radius=3),self.text(k,10,color=MUTED)]) for k,c in COLORS.items()])
  grid=[]
  for period in range(1,8):
   row=[]
   for group in range(1,19):
    e=next((x for x in elems if x.period==period and x.group==group and x.number not in range(58,72) and x.number not in range(90,104) and (self.category=="Todos" or self.category=="Favoritos" and x.number in self.favorites or self.category=="Metales" and x.category not in ("No metal","Gas noble","Metaloide","Halógeno") or self.category=="No metales" and x.category in ("No metal","Gas noble","Halógeno") or self.category=="Metaloides" and x.category=="Metaloide" or self.category=="Gases nobles" and x.category=="Gas noble")),None)
    if e: row.append(self.element_tile(e))
    else: row.append(ft.Container(width=64,height=72))
   grid.append(ft.Row(spacing=4,controls=row))
  frows=[]
  for start,end in [(57,71),(89,103)]: frows.append(ft.Row(spacing=4,controls=[ft.Container(width=64) for _ in range(3)]+[self.element_tile(e) for e in elems if start<=e.number<=end]))
  return ft.Column(spacing=14,controls=[self.header("Tabla periódica",f"{len(elems)} elementos"),tabs,legend,*grid,*frows])
 def set_category(self,c): self.category=c; self.refresh()
 def select(self,n): self.selected=n; self.route="Buscar"; self.refresh()
 def element_card(self,e,button=True):
  tile=ft.Container(width=48,height=52,bgcolor=COLORS.get(e.category,"#E5E8EF"),border_radius=7,padding=6,content=ft.Column(spacing=0,controls=[self.text(e.number,9),self.text(e.symbol,19,ft.FontWeight.BOLD)]))
  body=ft.Row(controls=[tile,ft.Column(expand=True,spacing=2,controls=[self.text(e.name,16,ft.FontWeight.BOLD),self.text(e.category)]) ,self.text(f"{e.atomic_mass or '—'} u",12,color=MUTED)],vertical_alignment=ft.CrossAxisAlignment.CENTER)
  if button: body.controls.append(self.btn("Ver detalle",lambda ev,n=e.number:self.show_detail(n)))
  return self.card(body)
 def show_detail(self,n): self.selected=n; self.refresh()
 def format_temp(self,value):
  if value is None: return "No disponible"
  unit=self.settings["Temperatura"]
  if unit=="°C": return f"{value-273.15:.2f} °C"
  if unit=="°F": return f"{(value-273.15)*9/5+32:.2f} °F"
  return f"{value:g} K"
 def detail_panel(self,e):
  if not e:return self.card(self.text("Selecciona un elemento para ver sus propiedades",color=MUTED))
  props=[("Grupo / Período",f"{e.group} · {e.period}"),("Bloque",e.block),("Masa atómica",e.atomic_mass or "No disponible"),("Configuración electrónica",e.electron_configuration or "No disponible"),("Electronegatividad",e.electronegativity or "No disponible"),("Punto de fusión",self.format_temp(e.melting_point)),("Punto de ebullición",self.format_temp(e.boiling_point)),("Densidad",f"{e.density} {e.density_unit}" if e.density is not None else "No disponible"),("Estado",e.phase or "No disponible")]
  return self.card(ft.Column(controls=[self.text("SELECCIONADO",10,color=MUTED),self.text(f"{e.number}  {e.name} ({e.symbol})",18,ft.FontWeight.BOLD),*[ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN,controls=[self.text(k,color=MUTED),self.text(v,weight=ft.FontWeight.BOLD)]) for k,v in props],self.btn("★ Favorito",lambda ev:self.toggle_favorite(e.number)),self.btn("Comparar",lambda ev:self.add_compare(e.number)),self.btn("Abrir en Tabla",lambda ev:self.go("Tabla"),True)],spacing=10))
 def search_view(self):
  q=ft.TextField(label="Por nombre, símbolo o número atómico",value=self.query,on_change=lambda e:self.set_query(e.control.value),expand=True)
  results=self.service.filter(self.service.search(self.query),category=self.search_category,block=self.search_block,period=self.search_period)
  category_buttons=ft.Row(wrap=True,spacing=6,controls=[self.btn(label,lambda ev,v=value:self.set_search_filter("category",v),self.search_category==value) for label,value in [("Todas",None),("No metal","No metal"),("Transición","Transición"),("Gas noble","Gas noble"),("Alcalino","Alcalino"),("Halógeno","Halógeno"),("Metaloide","Metaloide"),("Lantánido","Lantánido"),("Actínido","Actínido")]])
  block_buttons=ft.Row(wrap=True,spacing=6,controls=[self.btn(label,lambda ev,v=value:self.set_search_filter("block",v),self.search_block==value) for label,value in [("Todos los bloques",None),("s","s"),("p","p"),("d","d"),("f","f")]])
  period_buttons=ft.Row(wrap=True,spacing=6,controls=[self.btn(label,lambda ev,v=value:self.set_search_filter("period",v),self.search_period==value) for label,value in [("Todos los períodos",None)]+[(f"Período {n}",n) for n in range(1,8)]])
  return ft.Column(spacing=14,controls=[self.header("Buscar elementos","Encuentra por nombre, símbolo o número atómico"),ft.Row(controls=[q,self.btn("Buscar",lambda ev:self.refresh(),True)]),self.text("Filtros · Categoría",12,color=MUTED),category_buttons,self.text("Bloque",12,color=MUTED),block_buttons,self.text("Período",12,color=MUTED),period_buttons,self.text(f"{len(results)} resultados · ordenar por número atómico",12,color=MUTED),ft.Row(vertical_alignment=ft.CrossAxisAlignment.START,spacing=16,controls=[ft.Column(expand=True,controls=[self.element_card(e) for e in results[:60]],spacing=8),ft.Container(width=310,content=self.detail_panel(self.service.get(self.selected) if self.selected else None))])])
 def set_query(self,q): self.query=q; self.refresh()
 def set_search_filter(self,key,value):
  if key=="category": self.search_category=value
  elif key=="block": self.search_block=value
  elif key=="period": self.search_period=value
  self.refresh()
 def add_compare(self,n):
  if not self.compare.toggle(n): self.page.snack_bar=ft.SnackBar(ft.Text("Puedes comparar hasta 4 elementos")); self.page.snack_bar.open=True
  self.go("Comparar")
 def compare_view(self):
  selected=[self.service.get(n) for n in self.compare.numbers]
  cards=[]
  for e in selected:
   cards.append(self.card(ft.Column(controls=[self.element_card(e,False),*[ft.Column(spacing=1,controls=[self.text(k,10,color=MUTED),self.text(v,14,ft.FontWeight.BOLD)]) for k,v in [("Masa atómica",e.atomic_mass or "—"),("Categoría",e.category),("Configuración",e.electron_configuration or "—"),("Electronegatividad",e.electronegativity or "—"),("Fusión",self.format_temp(e.melting_point)),("Densidad",f"{e.density} {e.density_unit}" if e.density is not None else "—")]],self.btn("Quitar",lambda ev,n=e.number:self.remove_compare(n))],spacing=10),padding=12))
  add=self.card(ft.Column(alignment=ft.MainAxisAlignment.CENTER,horizontal_alignment=ft.CrossAxisAlignment.CENTER,controls=[self.text(f"{4-len(selected)} espacios disponibles",12),self.btn("+ Añadir",lambda ev:self.go("Buscar"),True)]))
  return ft.Column(spacing=16,controls=[self.header("Comparar elementos","Compara propiedades lado a lado · hasta 4 elementos"),ft.Row(wrap=True,vertical_alignment=ft.CrossAxisAlignment.START,controls=cards+[add]),self.card(ft.Column(controls=[self.text("UBICACIÓN EN LA TABLA",12,ft.FontWeight.BOLD),*[self.text(f"{e.name}: grupo {e.group} · período {e.period}") for e in selected],self.btn("Limpiar comparación",lambda e:self.clear_compare())]))])
 def remove_compare(self,n): self.compare.toggle(n); self.refresh()
 def clear_compare(self): self.compare.clear(); self.refresh()
 def toggle_favorite(self,n):
  self.favorites.symmetric_difference_update({n}); self.refresh()
 def favorites_view(self):
  elems=[self.service.get(n) for n in sorted(self.favorites)]
  return ft.Column(spacing=14,controls=[self.header("Favoritos","Tus elementos guardados y sus notas"),ft.Text(f"{len(elems)} elementos guardados"),ft.Row(wrap=True,controls=[self.card(ft.Column(controls=[self.element_card(e,False),ft.TextField(label="Añadir una nota",value=self.notes.get(e.number,""),on_change=lambda ev,n=e.number:self.save_note(n,ev.control.value)),self.btn("Quitar",lambda ev,n=e.number:self.toggle_favorite(n))])) for e in elems]) if elems else self.card(self.text("Aún no tienes favoritos. Abre un elemento y pulsa Favorito.",color=MUTED))])
 def save_note(self,n,v): self.notes[n]=v
 def quiz_view(self):
  pool=self.service.all()[:36]; target=pool[self.quiz_index%len(pool)]; prompt=f"¿Cuál es el símbolo de {target.name}?" if self.quiz_mode=="Símbolos" else f"¿Qué elemento tiene el símbolo {target.symbol}?" if self.quiz_mode=="Nombres" else f"¿Cuál es la categoría de {target.name}?"
  correct=target.symbol if self.quiz_mode=="Símbolos" else target.name if self.quiz_mode=="Nombres" else target.category
  choices=[correct]+[ (e.symbol if self.quiz_mode=="Símbolos" else e.name if self.quiz_mode=="Nombres" else e.category) for e in random.sample([x for x in pool if x.number!=target.number],3)]
  random.Random(self.quiz_index).shuffle(choices)
  options=ft.RadioGroup(value=self.quiz_selected,on_change=lambda ev:self.set_quiz_answer(ev.control.value),content=ft.Column(controls=[ft.Radio(value=v,label=f"{chr(65+i)}   {v}") for i,v in enumerate(choices)]))
  return ft.Column(spacing=16,controls=[self.header("Quiz","Practica símbolos, nombres y categorías"),ft.Row(controls=[self.btn(m,lambda ev,x=m:self.set_quiz_mode(x),self.quiz_mode==m) for m in ["Símbolos","Nombres","Categorías"]]),self.card(ft.Column(controls=[self.text(f"Pregunta {self.quiz_index+1}",12,color=MUTED),self.text(prompt,24,ft.FontWeight.BOLD),options,self.btn("Comprobar",lambda ev:self.check_quiz(target,correct),True),self.text(f"Puntuación: {self.score} · Racha: {self.streak} · Mejor: {self.best}")],spacing=18))])
 def set_quiz_mode(self,m): self.quiz_mode=m; self.refresh()
 def set_quiz_answer(self,value): self.quiz_selected=value
 def check_quiz(self,target,correct):
  if self.quiz_selected is None:
   self.page.snack_bar=ft.SnackBar(ft.Text("Selecciona una respuesta primero."))
   self.page.snack_bar.open=True
   return
  is_correct=self.quiz_selected==correct
  if is_correct:
   self.score+=1
   self.streak+=1
   self.best=max(self.best,self.streak)
  else:
   self.streak=0
  self.page.snack_bar=ft.SnackBar(ft.Text(("Correcto" if is_correct else "Incorrecto")+f" · Respuesta: {correct}"))
  self.page.snack_bar.open=True
  self.quiz_index+=1
  self.quiz_selected=None
  self.refresh()
 def settings_view(self):
  rows=[]
  for key,opts in [("Tema",["Claro","Oscuro","Sistema"]),("Idioma",["Español","English"]),("Temperatura",["K","°C","°F"]),("Tamaño",["Compacto","Normal","Grande"]),("Colores",["Sí","No"])]:
   rows.append(self.card(ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN,controls=[self.text(key,15,ft.FontWeight.BOLD),ft.Row(controls=[self.btn(x,lambda ev,k=key,v=x:self.set_setting(k,v),self.settings[key]==(True if key=="Colores" and x=="Sí" else False if key=="Colores" else x)) for x in opts]) ])))
  return ft.Column(spacing=12,controls=[self.header("Ajustes","Preferencias de la aplicación"),*rows,self.card(ft.Column(controls=[self.text("Datos",16,ft.FontWeight.BOLD),self.text("Fuente: src/data/elements.json"),self.text(f"Elementos: {len(self.service.all())}"),self.text("Datos de propiedades y unidades cargados desde el archivo JSON."),self.btn("Recargar datos",lambda ev:self.reload_data()),self.btn("Restablecer ajustes",lambda ev:self.reset_settings())]))])
 def set_setting(self,k,v): self.settings[k]=(v=="Sí") if k=="Colores" else v; self.page.theme_mode=ft.ThemeMode.DARK if self.settings["Tema"]=="Oscuro" else ft.ThemeMode.LIGHT; self.refresh()
 def reload_data(self): self.repo.reload(); self.refresh()
 def reset_settings(self): self.settings={"Tema":"Claro","Idioma":"Español","Temperatura":"K","Tamaño":"Normal","Colores":True}; self.refresh()

def main(page:ft.Page): PeriodicTableApp(page)
