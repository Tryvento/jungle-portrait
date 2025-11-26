import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
import os
import sys
from pathlib import Path
import shutil
from PIL import Image
import mimetypes

class ProjectManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestor de Proyecto Web - Productos y Promos")
        self.root.geometry("900x700")
        
        self.project_path = None
        self.products_data = {"products": []}
        self.promos_data = []
        
        self.setup_ui()
        
    def setup_ui(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Selección de carpeta
        ttk.Label(main_frame, text="Carpeta del Proyecto:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.path_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.path_var, width=50).grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5)
        ttk.Button(main_frame, text="Seleccionar Carpeta", command=self.select_folder).grid(row=0, column=2, padx=5)
        
        # Notebook para pestañas
        notebook = ttk.Notebook(main_frame)
        notebook.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        
        # Pestaña de Productos
        products_frame = ttk.Frame(notebook, padding="10")
        notebook.add(products_frame, text="Productos")
        
        # Pestaña de Promociones
        promos_frame = ttk.Frame(notebook, padding="10")
        notebook.add(promos_frame, text="Promociones")
        
        # Configurar las pestañas
        self.setup_products_tab(products_frame)
        self.setup_promos_tab(promos_frame)
        
        # Configurar grid expansion
        main_frame.rowconfigure(1, weight=1)
        
    def setup_products_tab(self, parent):
        # Frame para lista de productos
        list_frame = ttk.Frame(parent)
        list_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        ttk.Label(list_frame, text="Productos Existentes:").grid(row=0, column=0, sticky=tk.W)
        
        self.products_listbox = tk.Listbox(list_frame, width=30, height=15)
        self.products_listbox.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.products_listbox.bind('<<ListboxSelect>>', self.on_product_select)
        
        # Botones para productos
        btn_frame = ttk.Frame(list_frame)
        btn_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Button(btn_frame, text="Nuevo Producto", command=self.new_product).grid(row=0, column=0, padx=2)
        ttk.Button(btn_frame, text="Eliminar Producto", command=self.delete_product).grid(row=0, column=1, padx=2)
        ttk.Button(btn_frame, text="Actualizar Lista", command=self.load_project_data).grid(row=0, column=2, padx=2)
        
        # Frame para edición de producto
        edit_frame = ttk.LabelFrame(parent, text="Editar Producto", padding="10")
        edit_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        edit_frame.columnconfigure(1, weight=1)
        
        # Campos del formulario
        ttk.Label(edit_frame, text="ID (único):").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.product_id = ttk.Entry(edit_frame)
        self.product_id.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=2)
        
        ttk.Label(edit_frame, text="Nombre:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.product_name = ttk.Entry(edit_frame)
        self.product_name.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=2)
        
        ttk.Label(edit_frame, text="Precio:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.product_price = ttk.Entry(edit_frame)
        self.product_price.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=2)
        
        ttk.Label(edit_frame, text="Carpeta (para imágenes):").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.product_folder = ttk.Entry(edit_frame)
        self.product_folder.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=2)
        
        # Imágenes
        ttk.Label(edit_frame, text="Imágenes:", font=('Arial', 10, 'bold')).grid(row=4, column=0, columnspan=2, sticky=tk.W, pady=(10, 2))
        
        ttk.Label(edit_frame, text="Frontal:").grid(row=5, column=0, sticky=tk.W, pady=2)
        img_frame1 = ttk.Frame(edit_frame)
        img_frame1.grid(row=5, column=1, sticky=(tk.W, tk.E), pady=2)
        self.product_front = ttk.Entry(img_frame1)
        self.product_front.grid(row=0, column=0, sticky=(tk.W, tk.E))
        ttk.Button(img_frame1, text="Subir", width=6, command=lambda: self.upload_product_image("front")).grid(row=0, column=1, padx=2)
        
        ttk.Label(edit_frame, text="Posterior:").grid(row=6, column=0, sticky=tk.W, pady=2)
        img_frame2 = ttk.Frame(edit_frame)
        img_frame2.grid(row=6, column=1, sticky=(tk.W, tk.E), pady=2)
        self.product_back = ttk.Entry(img_frame2)
        self.product_back.grid(row=0, column=0, sticky=(tk.W, tk.E))
        ttk.Button(img_frame2, text="Subir", width=6, command=lambda: self.upload_product_image("back")).grid(row=0, column=1, padx=2)
        
        ttk.Label(edit_frame, text="Wallpaper:").grid(row=7, column=0, sticky=tk.W, pady=2)
        img_frame3 = ttk.Frame(edit_frame)
        img_frame3.grid(row=7, column=1, sticky=(tk.W, tk.E), pady=2)
        self.product_wallpaper = ttk.Entry(img_frame3)
        self.product_wallpaper.grid(row=0, column=0, sticky=(tk.W, tk.E))
        ttk.Button(img_frame3, text="Subir", width=6, command=lambda: self.upload_product_image("wallpaper")).grid(row=0, column=1, padx=2)
        
        # Previsualización de imágenes
        ttk.Label(edit_frame, text="Previsualización:", font=('Arial', 10, 'bold')).grid(row=8, column=0, columnspan=2, sticky=tk.W, pady=(10, 2))
        self.preview_label = ttk.Label(edit_frame, text="Selecciona una imagen para previsualizar", background="white", relief="solid")
        self.preview_label.grid(row=9, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=2, ipady=20)
        
        # Botón guardar
        ttk.Button(edit_frame, text="Guardar Producto", command=self.save_product).grid(row=10, column=0, columnspan=2, pady=10)
        
        # Configurar grid weights
        parent.columnconfigure(1, weight=1)
        parent.rowconfigure(0, weight=1)
        list_frame.rowconfigure(1, weight=1)
        list_frame.columnconfigure(0, weight=1)
        edit_frame.columnconfigure(1, weight=1)
        img_frame1.columnconfigure(0, weight=1)
        img_frame2.columnconfigure(0, weight=1)
        img_frame3.columnconfigure(0, weight=1)
        
    def setup_promos_tab(self, parent):
        # Frame para lista de promos
        list_frame = ttk.Frame(parent)
        list_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        ttk.Label(list_frame, text="Promociones Existentes:").grid(row=0, column=0, sticky=tk.W)
        
        self.promos_listbox = tk.Listbox(list_frame, width=30, height=15)
        self.promos_listbox.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.promos_listbox.bind('<<ListboxSelect>>', self.on_promo_select)
        
        # Botones para promos
        btn_frame = ttk.Frame(list_frame)
        btn_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Button(btn_frame, text="Nueva Promo", command=self.new_promo).grid(row=0, column=0, padx=2)
        ttk.Button(btn_frame, text="Eliminar Promo", command=self.delete_promo).grid(row=0, column=1, padx=2)
        ttk.Button(btn_frame, text="Actualizar Lista", command=self.load_project_data).grid(row=0, column=2, padx=2)
        
        # Frame para edición de promo
        edit_frame = ttk.LabelFrame(parent, text="Editar Promoción", padding="10")
        edit_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        edit_frame.columnconfigure(1, weight=1)
        
        # Campos del formulario
        ttk.Label(edit_frame, text="Archivo:").grid(row=0, column=0, sticky=tk.W, pady=2)
        file_frame = ttk.Frame(edit_frame)
        file_frame.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=2)
        self.promo_src = ttk.Entry(file_frame)
        self.promo_src.grid(row=0, column=0, sticky=(tk.W, tk.E))
        ttk.Button(file_frame, text="Subir", width=6, command=self.upload_promo_file).grid(row=0, column=1, padx=2)
        
        ttk.Label(edit_frame, text="Texto alternativo:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.promo_alt = ttk.Entry(edit_frame)
        self.promo_alt.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=2)
        
        ttk.Label(edit_frame, text="Tipo:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.promo_type = ttk.Combobox(edit_frame, values=["image", "video"], state="readonly")
        self.promo_type.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=2)
        self.promo_type.set("image")
        
        # Previsualización
        ttk.Label(edit_frame, text="Previsualización:", font=('Arial', 10, 'bold')).grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=(10, 2))
        self.promo_preview_label = ttk.Label(edit_frame, text="Selecciona un archivo para previsualizar", background="white", relief="solid")
        self.promo_preview_label.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=2, ipady=40)
        
        # Botón guardar
        ttk.Button(edit_frame, text="Guardar Promoción", command=self.save_promo).grid(row=5, column=0, columnspan=2, pady=10)
        
        # Configurar grid weights
        parent.columnconfigure(1, weight=1)
        parent.rowconfigure(0, weight=1)
        list_frame.rowconfigure(1, weight=1)
        list_frame.columnconfigure(0, weight=1)
        edit_frame.columnconfigure(1, weight=1)
        file_frame.columnconfigure(0, weight=1)
        
    def select_folder(self):
        folder = filedialog.askdirectory(title="Seleccionar carpeta del proyecto")
        if folder:
            self.project_path = folder
            self.path_var.set(folder)
            self.load_project_data()
            
    def load_project_data(self):
        if not self.project_path:
            return
            
        try:
            # Cargar productos
            products_file = os.path.join(self.project_path, "assets", "data", "products.json")
            if os.path.exists(products_file):
                with open(products_file, 'r', encoding='utf-8') as f:
                    self.products_data = json.load(f)
                self.update_products_list()
            
            # Cargar promociones
            promos_file = os.path.join(self.project_path, "assets", "data", "promo.json")
            if os.path.exists(promos_file):
                with open(promos_file, 'r', encoding='utf-8') as f:
                    self.promos_data = json.load(f)
                self.update_promos_list()
                
            messagebox.showinfo("Éxito", "Proyecto cargado correctamente")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar el proyecto: {str(e)}")
    
    def update_products_list(self):
        self.products_listbox.delete(0, tk.END)
        for product in self.products_data["products"]:
            self.products_listbox.insert(tk.END, f"{product['id']} - {product['name']}")
    
    def update_promos_list(self):
        self.promos_listbox.delete(0, tk.END)
        for promo in self.promos_data:
            filename = os.path.basename(promo['src'])
            self.promos_listbox.insert(tk.END, f"{filename} - {promo['alt']}")
    
    def on_product_select(self, event):
        selection = self.products_listbox.curselection()
        if selection:
            index = selection[0]
            product = self.products_data["products"][index]
            
            self.product_id.delete(0, tk.END)
            self.product_id.insert(0, product.get('id', ''))
            
            self.product_name.delete(0, tk.END)
            self.product_name.insert(0, product.get('name', ''))
            
            self.product_price.delete(0, tk.END)
            self.product_price.insert(0, product.get('price', ''))
            
            self.product_folder.delete(0, tk.END)
            self.product_folder.insert(0, product.get('folder', ''))
            
            images = product.get('images', {})
            self.product_front.delete(0, tk.END)
            self.product_front.insert(0, images.get('front', ''))
            
            self.product_back.delete(0, tk.END)
            self.product_back.insert(0, images.get('back', ''))
            
            self.product_wallpaper.delete(0, tk.END)
            self.product_wallpaper.insert(0, images.get('wallpaper', ''))
            
            # Previsualizar primera imagen
            if images.get('front'):
                self.preview_image(images.get('front'))
    
    def on_promo_select(self, event):
        selection = self.promos_listbox.curselection()
        if selection:
            index = selection[0]
            promo = self.promos_data[index]
            
            self.promo_src.delete(0, tk.END)
            self.promo_src.insert(0, promo.get('src', ''))
            
            self.promo_alt.delete(0, tk.END)
            self.promo_alt.insert(0, promo.get('alt', ''))
            
            self.promo_type.set(promo.get('type', 'image'))
            
            # Previsualizar
            if promo.get('src'):
                self.preview_promo(promo.get('src'))
    
    def new_product(self):
        # Limpiar formulario
        for widget in [self.product_id, self.product_name, self.product_price, self.product_folder,
                      self.product_front, self.product_back, self.product_wallpaper]:
            widget.delete(0, tk.END)
        self.preview_label.config(text="Selecciona una imagen para previsualizar")
    
    def new_promo(self):
        self.promo_src.delete(0, tk.END)
        self.promo_alt.delete(0, tk.END)
        self.promo_type.set("image")
        self.promo_preview_label.config(text="Selecciona un archivo para previsualizar")
    
    def delete_product(self):
        selection = self.products_listbox.curselection()
        if selection:
            index = selection[0]
            product = self.products_data["products"][index]
            product_name = product["name"]
            
            if messagebox.askyesno("Confirmar", f"¿Eliminar el producto '{product_name}'?"):
                # Opcional: eliminar imágenes del producto
                if messagebox.askyesno("Eliminar imágenes", "¿Deseas también eliminar las imágenes asociadas a este producto?"):
                    self.delete_product_images(product)
                
                self.products_data["products"].pop(index)
                self.update_products_list()
                self.save_all_data()
                self.new_product()  # Limpiar formulario
    
    def delete_promo(self):
        selection = self.promos_listbox.curselection()
        if selection:
            index = selection[0]
            promo = self.promos_data[index]
            promo_alt = promo["alt"]
            
            if messagebox.askyesno("Confirmar", f"¿Eliminar la promoción '{promo_alt}'?"):
                # Opcional: eliminar archivo de promoción
                if messagebox.askyesno("Eliminar archivo", "¿Deseas también eliminar el archivo asociado a esta promoción?"):
                    self.delete_promo_file(promo)
                
                self.promos_data.pop(index)
                self.update_promos_list()
                self.save_all_data()
                self.new_promo()  # Limpiar formulario
    
    def delete_product_images(self, product):
        """Elimina las imágenes asociadas a un producto"""
        try:
            images = product.get('images', {})
            for image_type, image_path in images.items():
                if image_path and not image_path.startswith(('http://', 'https://')):
                    full_path = os.path.join(self.project_path, image_path.lstrip('/'))
                    if os.path.exists(full_path):
                        os.remove(full_path)
                        print(f"Eliminada: {full_path}")
        except Exception as e:
            print(f"Error eliminando imágenes: {e}")
    
    def delete_promo_file(self, promo):
        """Elimina el archivo asociado a una promoción"""
        try:
            src = promo.get('src', '')
            if src and not src.startswith(('http://', 'https://')):
                full_path = os.path.join(self.project_path, src.lstrip('/'))
                if os.path.exists(full_path):
                    os.remove(full_path)
                    print(f"Eliminada: {full_path}")
        except Exception as e:
            print(f"Error eliminando archivo de promo: {e}")
    
    def upload_product_image(self, image_type):
        if not self.project_path:
            messagebox.showwarning("Advertencia", "Primero selecciona la carpeta del proyecto")
            return
            
        file_path = filedialog.askopenfilename(
            title=f"Seleccionar imagen {image_type}",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp")]
        )
        
        if file_path:
            # Obtener carpeta del producto
            folder_name = self.product_folder.get() or "default"
            if not folder_name:
                folder_name = "default"
            
            # Crear estructura de carpetas
            product_images_dir = os.path.join(self.project_path, "assets", "img", "Phones", folder_name)
            os.makedirs(product_images_dir, exist_ok=True)
            
            # Copiar archivo
            filename = f"{folder_name}-{image_type}{os.path.splitext(file_path)[1]}"
            dest_path = os.path.join(product_images_dir, filename)
            
            try:
                shutil.copy2(file_path, dest_path)
                
                # Ruta relativa para el JSON
                rel_path = os.path.relpath(dest_path, self.project_path).replace('\\', '/')
                
                if image_type == "front":
                    self.product_front.delete(0, tk.END)
                    self.product_front.insert(0, rel_path)
                elif image_type == "back":
                    self.product_back.delete(0, tk.END)
                    self.product_back.insert(0, rel_path)
                elif image_type == "wallpaper":
                    self.product_wallpaper.delete(0, tk.END)
                    self.product_wallpaper.insert(0, rel_path)
                
                # Previsualizar
                self.preview_image(rel_path)
                
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo subir la imagen: {str(e)}")
    
    def upload_promo_file(self):
        if not self.project_path:
            messagebox.showwarning("Advertencia", "Primero selecciona la carpeta del proyecto")
            return
            
        file_path = filedialog.askopenfilename(
            title="Seleccionar archivo de promoción",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp"), ("Video files", "*.mp4 *.avi *.mov")]
        )
        
        if file_path:
            # Crear directorio de marketing
            marketing_dir = os.path.join(self.project_path, "assets", "img", "marketing")
            os.makedirs(marketing_dir, exist_ok=True)
            
            # Copiar archivo
            filename = os.path.basename(file_path)
            dest_path = os.path.join(marketing_dir, filename)
            
            try:
                shutil.copy2(file_path, dest_path)
                
                # Ruta relativa para el JSON
                rel_path = os.path.relpath(dest_path, self.project_path).replace('\\', '/')
                
                self.promo_src.delete(0, tk.END)
                self.promo_src.insert(0, rel_path)
                
                # Auto-detectar tipo
                if file_path.lower().endswith(('.mp4', '.avi', '.mov')):
                    self.promo_type.set("video")
                else:
                    self.promo_type.set("image")
                
                # Previsualizar
                self.preview_promo(rel_path)
                
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo subir el archivo: {str(e)}")
    
    def preview_image(self, image_path):
        """Previsualiza una imagen en la interfaz"""
        try:
            if not image_path or not self.project_path:
                return
                
            full_path = os.path.join(self.project_path, image_path.lstrip('/'))
            if os.path.exists(full_path):
                # Para una implementación real, podrías usar PIL para redimensionar y mostrar
                filename = os.path.basename(image_path)
                self.preview_label.config(text=f"Imagen: {filename}\nRuta: {image_path}")
            else:
                self.preview_label.config(text="Imagen no encontrada en el proyecto")
        except Exception as e:
            self.preview_label.config(text=f"Error al cargar previsualización: {str(e)}")
    
    def preview_promo(self, file_path):
        """Previsualiza un archivo de promoción"""
        try:
            if not file_path or not self.project_path:
                return
                
            full_path = os.path.join(self.project_path, file_path.lstrip('/'))
            if os.path.exists(full_path):
                filename = os.path.basename(file_path)
                file_type = "Video" if file_path.lower().endswith(('.mp4', '.avi', '.mov')) else "Imagen"
                self.promo_preview_label.config(text=f"{file_type}: {filename}\nRuta: {file_path}")
            else:
                self.promo_preview_label.config(text="Archivo no encontrado en el proyecto")
        except Exception as e:
            self.promo_preview_label.config(text=f"Error al cargar previsualización: {str(e)}")
    
    def save_product(self):
        if not self.project_path:
            messagebox.showwarning("Advertencia", "Primero selecciona la carpeta del proyecto")
            return
            
        # Validar campos obligatorios
        if not all([self.product_id.get(), self.product_name.get(), self.product_price.get()]):
            messagebox.showwarning("Advertencia", "ID, Nombre y Precio son obligatorios")
            return
        
        # Buscar si ya existe el producto
        product_id = self.product_id.get()
        existing_index = None
        for i, product in enumerate(self.products_data["products"]):
            if product["id"] == product_id:
                existing_index = i
                break
        
        product_data = {
            "id": product_id,
            "name": self.product_name.get(),
            "price": self.product_price.get(),
            "folder": self.product_folder.get() or product_id,
            "images": {
                "front": self.product_front.get(),
                "back": self.product_back.get(),
                "wallpaper": self.product_wallpaper.get()
            }
        }
        
        if existing_index is not None:
            # Actualizar producto existente
            self.products_data["products"][existing_index] = product_data
        else:
            # Agregar nuevo producto
            self.products_data["products"].append(product_data)
        
        self.update_products_list()
        self.save_all_data()
        messagebox.showinfo("Éxito", "Producto guardado correctamente")
    
    def save_promo(self):
        if not self.project_path:
            messagebox.showwarning("Advertencia", "Primero selecciona la carpeta del proyecto")
            return
            
        if not all([self.promo_src.get(), self.promo_alt.get()]):
            messagebox.showwarning("Advertencia", "Archivo y texto alternativo son obligatorios")
            return
        
        promo_data = {
            "src": self.promo_src.get(),
            "alt": self.promo_alt.get(),
            "type": self.promo_type.get()
        }
        
        # Buscar si ya existe la promo (por src)
        existing_index = None
        for i, promo in enumerate(self.promos_data):
            if promo["src"] == promo_data["src"]:
                existing_index = i
                break
        
        if existing_index is not None:
            # Actualizar promo existente
            self.promos_data[existing_index] = promo_data
        else:
            # Agregar nueva promo
            self.promos_data.append(promo_data)
        
        self.update_promos_list()
        self.save_all_data()
        messagebox.showinfo("Éxito", "Promoción guardada correctamente")
    
    def save_all_data(self):
        if not self.project_path:
            return
            
        try:
            # Asegurar que existan los directorios
            data_dir = os.path.join(self.project_path, "assets", "data")
            os.makedirs(data_dir, exist_ok=True)
            
            # Guardar productos
            products_file = os.path.join(data_dir, "products.json")
            with open(products_file, 'w', encoding='utf-8') as f:
                json.dump(self.products_data, f, indent=2, ensure_ascii=False)
            
            # Guardar promociones
            promos_file = os.path.join(data_dir, "promo.json")
            with open(promos_file, 'w', encoding='utf-8') as f:
                json.dump(self.promos_data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar los datos: {str(e)}")

def main():
    root = tk.Tk()
    app = ProjectManager(root)
    root.mainloop()

if __name__ == "__main__":
    main()