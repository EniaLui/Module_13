import asyncio
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import State, StatesGroup

api = "тут ключ от бота"
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

    @dp.message_handler(commands=['start'])
    async def start(message: types.Message):
        await message.answer(
            "Привет! Я бот, помогающий твоему здоровью.\nВведите 'Calories', чтобы рассчитать норму калорий.")

    @dp.message_handler(lambda message: message.text.lower() == 'calories')
    async def set_age(message: types.Message):
        await message.answer("Введите свой возраст:")
        await UserState.age.set()

    @dp.message_handler(state=UserState.age)
    async def set_growth(message: types.Message):
        await state.update_data(age=int(message.text))
        await message.answer("Введите свой рост (в см):")
        await UserState.growth.set()

    @dp.message_handler(state=UserState.growth)
    async def set_weight(message: types.Message):
        await state.update_data(growth=int(message.text))
        await message.answer("Введите свой вес (в кг):")
        await UserState.weight.set()

    @dp.message_handler(state=UserState.weight)
    async def send_calories(message: types.Message):
        await state.update_data(weight=int(message.text))
        data = await state.get_data()
        age = data['age']
        growth = data['growth']
        weight = data['weight']
            # Формула для женщин
        calories = 10 * weight + 6.25 * growth - 5 * age - 161
        await message.answer(f"Ваша норма калорий: {calories:.2f} ккал в сутки.")
        await state.finish()

    @dp.message_handler()
    async def all_messages(message: types.Message):
        await message.answer("Введите команду /start, чтобы начать общение.")

    if __name__ == "__main__":
        executor.start_polling(dp, skip_updates=True)
