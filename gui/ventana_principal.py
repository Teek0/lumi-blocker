# gui/ventana_principal.py

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QTabWidget, QPushButton, QSpinBox, QTimeEdit, QGroupBox
)
from PySide6.QtCore import Qt


class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LumiBlocker")
        self.setMinimumSize(800, 600)
        self._setup_ui()

    def _setup_ui(self):
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout principal
        layout = QVBoxLayout()

        # Crear pestañas
        self.tabs = QTabWidget()

        # Pestaña Modo
        self.tab_modo = self._crear_tab_modo()
        self.tabs.addTab(self.tab_modo, "🧠 Modo")

        # Pestañas vacías para Procesos, Webs, Logs
        self.tabs.addTab(QWidget(), "🚫 Procesos")
        self.tabs.addTab(QWidget(), "🌐 Webs")
        self.tabs.addTab(QWidget(), "📋 Logs")

        # Agregar pestañas al layout
        layout.addWidget(self.tabs)
        central_widget.setLayout(layout)

    def _crear_tab_modo(self):
        """Crea la pestaña para seleccionar y controlar los modos de bloqueo"""
        tab = QWidget()
        layout = QVBoxLayout()

        # --- Modo Temporizador ---
        grupo_temporizador = QGroupBox("Modo Temporizador")
        temp_layout = QVBoxLayout()

        # Input duración
        duracion_layout = QHBoxLayout()
        self.input_duracion = QSpinBox()
        self.input_duracion.setRange(1, 480)
        self.input_duracion.setValue(25)
        self.input_duracion.setSuffix(" minutos")
        duracion_layout.addWidget(QLabel("Duración:"))
        duracion_layout.addWidget(self.input_duracion)

        # Botones
        botones_temp = QHBoxLayout()
        self.boton_temp_iniciar = QPushButton("Iniciar")
        self.boton_temp_pausar = QPushButton("Pausar")
        self.boton_temp_detener = QPushButton("Detener")
        botones_temp.addWidget(self.boton_temp_iniciar)
        botones_temp.addWidget(self.boton_temp_pausar)
        botones_temp.addWidget(self.boton_temp_detener)

        # Estado
        self.label_estado_temp = QLabel("Sesión: No iniciada")
        self.label_estado_temp.setStyleSheet("color: #666;")

        # Armar layout
        temp_layout.addLayout(duracion_layout)
        temp_layout.addLayout(botones_temp)
        temp_layout.addWidget(self.label_estado_temp)
        grupo_temporizador.setLayout(temp_layout)

        # --- Modo Horario ---
        grupo_horario = QGroupBox("Modo Horario")
        horario_layout = QVBoxLayout()

        # Input horas
        horas_layout = QHBoxLayout()
        self.input_inicio = QTimeEdit()
        self.input_fin = QTimeEdit()
        horas_layout.addWidget(QLabel("Desde:"))
        horas_layout.addWidget(self.input_inicio)
        horas_layout.addWidget(QLabel("Hasta:"))
        horas_layout.addWidget(self.input_fin)

        # Botones
        botones_horario = QHBoxLayout()
        self.boton_horario_iniciar = QPushButton("Iniciar")
        self.boton_horario_pausar = QPushButton("Pausar")
        self.boton_horario_detener = QPushButton("Detener")
        botones_horario.addWidget(self.boton_horario_iniciar)
        botones_horario.addWidget(self.boton_horario_pausar)
        botones_horario.addWidget(self.boton_horario_detener)

        # Estado
        self.label_estado_horario = QLabel("Horario: Inactivo")
        self.label_estado_horario.setStyleSheet("color: #666;")

        # Armar layout
        horario_layout.addLayout(horas_layout)
        horario_layout.addLayout(botones_horario)
        horario_layout.addWidget(self.label_estado_horario)
        grupo_horario.setLayout(horario_layout)

        # --- Modo Permanente ---
        grupo_permanente = QGroupBox("Modo Permanente")
        permanente_layout = QVBoxLayout()

        # Botones
        botones_perm = QHBoxLayout()
        self.boton_perm_iniciar = QPushButton("Iniciar")
        self.boton_perm_detener = QPushButton("Detener")
        botones_perm.addWidget(self.boton_perm_iniciar)
        botones_perm.addWidget(self.boton_perm_detener)

        # Estado
        self.label_estado_perm = QLabel("Estado: Inactivo")
        self.label_estado_perm.setStyleSheet("color: #666;")

        # Armar layout
        permanente_layout.addLayout(botones_perm)
        permanente_layout.addWidget(self.label_estado_perm)
        grupo_permanente.setLayout(permanente_layout)

        # Agregar todos los grupos al layout principal
        layout.addWidget(grupo_temporizador)
        layout.addWidget(grupo_horario)
        layout.addWidget(grupo_permanente)
        layout.addStretch()

        tab.setLayout(layout)
        return tab



