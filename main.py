import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TMDB_API_KEY = "0ed1eb618a5d947f9ae8cce913bd6229"
TELEGRAM_TOKEN = "7982919097:AAG6eG-3avybE-yKdFRkEd8EXtmaqhmbvUE"

TMDB_BASE_URL = "https://api.themoviedb.org/3"
IMAGE_BASE_URL = "https://image.tmdb.org/t/p/original"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send /poster <movie name> or /backdrop <movie name>.")

def get_movie_data(query):
    url = f"{TMDB_BASE_URL}/search/movie"
    params = {
        "api_key": TMDB_API_KEY,
        "query": query,
        "language": "en-US"  # Fetch results in English
    }
    response = requests.get(url, params=params)
    if response.status_code == 200 and response.json()["results"]:
        return response.json()["results"][0]
    return None

async def poster(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = " ".join(context.args)
    if not query:
        await update.message.reply_text("Please provide a movie name.")
        return
    movie = get_movie_data(query)
    if movie and movie.get("poster_path"):
        image_url = IMAGE_BASE_URL + movie["poster_path"]
        await update.message.reply_photo(photo=image_url, caption=movie["title"])
    else:
        await update.message.reply_text("Poster not found.")

async def backdrop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = " ".join(context.args)
    if not query:
        await update.message.reply_text("Please provide a movie name.")
        return
    movie = get_movie_data(query)
    if movie and movie.get("backdrop_path"):
        # Fetch multiple backdrops
        backdrops = movie.get("backdrops", [])
        if backdrops:
            # Send up to 10 backdrops
            count = min(len(backdrops), 10)
            for i in range(count):
                backdrop_url = IMAGE_BASE_URL + backdrops[i]["file_path"]
                await update.message.reply_photo(photo=backdrop_url, caption=f"{movie['title']} - Backdrop {i+1}")
        else:
            await update.message.reply_text("No backdrops found.")
    else:
        await update.message.reply_text("Backdrop not found.")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("poster", poster))
    app.add_handler(CommandHandler("backdrop", backdrop))

    app.run_polling()
