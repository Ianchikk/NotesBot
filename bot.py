from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ParseMode
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

API_TOKEN = '6729565596:AAEoQzV134ofb2poJa5FzGCH1TPQkfu2sMI'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
logging_middleware = LoggingMiddleware()
dp.middleware.setup(logging_middleware)

Base = declarative_base()


class Note(Base):
    __tablename__ = 'notes'

    id = Column(Integer, primary_key=True)
    content = Column(String)

    def __repr__(self):
        return f"<Note(id={self.id}, content='{self.content}')>"


engine = create_engine('sqlite:///notes.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


@dp.message_handler(commands=['add'])
async def add_note(message: types.Message):
    content = message.get_args()
    if content:
        session = Session()
        new_note = Note(content=content)
        session.add(new_note)
        session.commit()
        session.close()
        await message.reply('Заметка добавлена!')
    else:
        await message.reply('Используйте команду в формате /add [Текст заметки]')


@dp.message_handler(commands=['getall'])
async def get_all_notes(message: types.Message):
    session = Session()
    notes = session.query(Note).all()
    session.close()
    if notes:
        response = '\n'.join(note.content for note in notes)
        await message.reply(response)
    else:
        await message.reply('Заметок пока нет')


if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
