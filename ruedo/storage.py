"""
ruedo/storage.py
Storage backend personalizado que sube archivos a Cloudinary.
Compatible con Django 6 sin depender de django-cloudinary-storage.
"""

import cloudinary
import cloudinary.uploader
from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible
import os


@deconstructible
class CloudinaryStorage(Storage):

    def _get_public_id(self, name):
        """Convierte el path del archivo en un public_id para Cloudinary."""
        # Quitar extensión — Cloudinary la maneja solo
        root, _ = os.path.splitext(name)
        return root.replace("\\", "/")

    def _open(self, name, mode="rb"):
        raise NotImplementedError("CloudinaryStorage no soporta abrir archivos directamente.")

    def _save(self, name, content):
        public_id = self._get_public_id(name)

        # Detectar si es video o imagen por extensión
        ext = os.path.splitext(name)[-1].lower()
        resource_type = "video" if ext in [".mp4", ".mov", ".avi", ".webm", ".mkv"] else "image"

        result = cloudinary.uploader.upload(
            content,
            public_id=public_id,
            resource_type=resource_type,
            overwrite=True,
        )
        # Guardar la URL segura como nombre — se usará en url()
        return result["secure_url"]

    def exists(self, name):
        # Cloudinary no tiene un método barato de verificación — asumir que no existe
        return False

    def url(self, name):
        # Si ya es una URL completa (guardada por _save) devolverla directo
        if name and name.startswith("http"):
            return name
        # Si es un path relativo construir la URL manualmente
        public_id = self._get_public_id(name)
        cloud_name = cloudinary.config().cloud_name
        return f"https://res.cloudinary.com/{cloud_name}/image/upload/{public_id}"

    def delete(self, name):
        try:
            public_id = self._get_public_id(name)
            cloudinary.uploader.destroy(public_id)
        except Exception:
            pass

    def size(self, name):
        return 0

    def path(self, name):
        raise NotImplementedError("CloudinaryStorage no usa rutas locales.")