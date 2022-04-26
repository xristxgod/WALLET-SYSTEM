from flask import Blueprint, redirect, url_for, render_template, request, flash

from src.services.favorites import FavoritesUsers

app = Blueprint("main", __name__)
favorites = FavoritesUsers()