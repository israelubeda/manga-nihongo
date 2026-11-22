# Manga Nihongo 📖

Programa de consola en español para aprender a leer japonés en Termux: hiragana, kanji, vocabulario habitual del manga y diálogos originales. Funciona sin conexión después de instalarlo. La interfaz usa [`color_latam`](https://pypi.org/project/color-latam/) para los colores ANSI.

## Instalación en Android (Termux)

Usa Termux actualizado y una fuente que muestre caracteres japoneses.

```sh
pkg update
pkg install python git
git clone https://github.com/israelubeda/manga-nihongo.git
cd manga-nihongo
python -m pip install .
manga-nihongo
```

Si prefieres ejecutarlo desde el código fuente:

```sh
PYTHONPATH=src python -m manga_nihongo
```

## Qué incluye

- 71 hiragana básicos y con dakuten/handakuten, con ejercicios de lectura en romaji y escritura en japonés.
- 75 kanji con significado, lectura de ejemplo y nota de otras lecturas. Un kanji puede tener muchas pronunciaciones; aquí se enseña una lectura frecuente en contexto, no una lista exhaustiva.
- 69 palabras y expresiones con traducción japonés → español, español → japonés y transcripción romaji.
- Tres escenas breves originales con revelación progresiva de traducción y notas de gramática.
- Repaso espaciado por tarjeta **y dirección**. Los aciertos duplican el intervalo hasta 60 días; los errores vuelven a un día.
- Diccionario local y estadísticas. El progreso se guarda en `~/.manga-nihongo/progreso.json`.

Se aceptan mayúsculas, espacios sobrantes y tildes opcionales en respuestas españolas. Para escribir japonés en Termux puedes activar un teclado japonés del sistema. En los ejercicios de romaji basta el teclado latino. Las traducciones pueden variar según el contexto; el programa evalúa las equivalencias indicadas en cada tarjeta.

## Uso rápido

```sh
manga-nihongo                       # menú interactivo
manga-nihongo --practicar hiragana  # ejercicios de hiragana
manga-nihongo --practicar kanji --cantidad 20
manga-nihongo --practicar vocabulario --nivel 2
manga-nihongo --repasar             # tarjetas vencidas
```

Durante una práctica: `?` muestra una pista, `/` revela la solución y `q` sale. Las respuestas omitidas se cuentan como error. `Ctrl+C` sale con seguridad.

Para elegir otra carpeta de progreso, define `MANGA_NIHONGO_HOME`, por ejemplo `export MANGA_NIHONGO_HOME="$HOME/Documents/manga"`.

## Ruta recomendada

1. Aprende las vocales y filas de hiragana en la sección 1. Practica hasta leer los caracteres sin ayuda.
2. Estudia vocabulario cotidiano y kanji básicos. Alterna japonés → español y español → japonés.
3. Lee las escenas sin revelar la traducción. Identifica partículas como `は` y `が`.
4. Revisa a diario las tarjetas pendientes; después intenta leer una viñeta real y busca palabras nuevas en el diccionario.

El contenido incluido es introductorio. Un manga real también usa katakana, vocabulario específico, conjugaciones, furigana y expresiones coloquiales. Esta versión se centra en establecer una base de lectura.

## Desarrollo

```sh
python -m pip install -e .
python -m unittest discover -s tests -v
```

## Licencia

MIT, emitida con el gestor de licencias de Israel Ubeda. Código interno **IU-OSS-0006**. Las condiciones legales están en [LICENSE](LICENSE) y el registro se identifica en [LICENSE_ID.txt](LICENSE_ID.txt).

