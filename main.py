import asyncio
import os
from dotenv import load_dotenv
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from keyboards import *
from JSONDATABASE import JsonDataLoader
from MySQLDatabase import DatabaseManager
from aiogram.fsm.state import StatesGroup, State
from datetime import datetime
import time
from aiogram import F
import json


class CleaningFSM(StatesGroup):
    choose_building = State() 
    
    #ПЕРВЫЙ АДРЕС
    floor_1_corridor = State()
    floor_1_restroom = State()
    floor_2_corridor = State()
    floor_2_restroom = State()
    stairsl1 = State()

    #ВТОРОЙ АДРЕС
    room_1 = State()
    room_6 = State()
    restroom = State()
    stairsl2 = State()
    corridor = State()

    additional_photo=State()


    consumabels = State()

    order = State()
    order_amount = State()

    toRepair = State()
    repair_photo = State()

    final = State()


def format_strings_as_column(strings):

    return  "\n".join(strings) + "\n"

load_dotenv()

token = os.getenv("TOKEN")

logging.basicConfig(level=logging.INFO)

loader = JsonDataLoader("./objects.json")
objects = loader.get_data()

db_manager = DatabaseManager("example.db")


bot = Bot(token=token)
dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    if not await db_manager.get_user_by_telegram_id(message.from_user.id):
        await message.answer(
            "Please share your phone number to continue.", 
            reply_markup=phone_request_keyboard
        )
    else:
        await message.answer("Здравствуйте, вы уже верифицированы. Для работы с ботом нажмите кнопку ниже.", reply_markup=start_cleaning_button())

@dp.message(lambda message: message.contact)
async def handle_contact(message: types.Message):
    if message.contact.user_id == message.from_user.id:
        await db_manager.add_user(message.contact.phone_number, message.from_user.id)
        await message.answer("Thank you! You are now verified.", reply_markup=start_cleaning_button())
    else:
        await message.answer("Please share your own phone number.")

@dp.message(F.text == "Начать уборку")
async def handle_start_cleaning(message: types.Message, state: FSMContext):
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    await state.update_data(startTime = formatted_datetime)
    await message.answer("Выберите строение для уборки:", reply_markup=building_keyboard())
    await state.set_state(CleaningFSM.choose_building) 

# @dp.message()
# async def fallback(message: types.Message):
#     if not await db_manager.get_user_by_telegram_id(message.from_user.id):
#         await message.answer(
#             "You need to share your phone number to use this bot.", 
#             reply_markup=phone_request_keyboard
#         )


#ВЫБОР АДРЕСА
@dp.message(CleaningFSM.choose_building)
async def choose_building_handler(message: types.Message, state: FSMContext):
    chosen_building = message.text

    await state.update_data(chosen_building=chosen_building)
    
    if chosen_building == "Пятницкая, 7A":
        await message.answer("📸 Отправьте фотографию коридора 1 этажа. При необходимости нажмите Пропустить.", reply_markup=skip_keyboard())
        await state.set_state(CleaningFSM.floor_1_corridor)
    elif chosen_building == "Свободы, 95к2":
        await message.answer("📸 Отправьте фотографию комнаты №1. При необходимости нажмите Пропустить.", reply_markup=skip_keyboard())
        await state.set_state(CleaningFSM.room_1)

#ФОТОГРАФИИ
#ПЕРВЫЙ АДРЕС
@dp.message(CleaningFSM.floor_1_corridor)
async def location_1_f1c(message: types.Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    photos = data.get("photos", [])

    if message.content_type == 'text' and message.text == "Пропустить":
        photos.append('skip')
    elif message.content_type == 'photo':
        photo = message.photo[-1]
        file_path = f"photos/{message.from_user.id}_location_1_{int(time.time())}.jpg"
        
        os.makedirs("photos", exist_ok=True)
        
        try:
            await bot.download(photo, destination=file_path)
            photos.append(file_path)
        except Exception as e:
            await message.answer("Произошла ошибка при загрузке фотографии. Попробуйте ещё раз.")
            return
    else:
        await message.answer("Пожалуйста, отправьте фотографию или нажмите 'Пропустить'.")
        return

    await state.update_data(photos=photos)
    await state.set_state(CleaningFSM.floor_1_restroom)
    await message.answer(
        "📸 Отправьте фотографию санузла 1 этажа. При необходимости нажмите Пропустить.",
        reply_markup=skip_keyboard(),
    )

@dp.message(CleaningFSM.floor_1_restroom)
async def location_1_f1r(message: types.Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    photos = data.get("photos", [])

    if message.content_type == 'text' and message.text == "Пропустить":
        photos.append('skip')
    elif message.content_type == 'photo':
        photo = message.photo[-1]
        file_path = f"photos/{message.from_user.id}_location_1_{int(time.time())}.jpg"
        
        os.makedirs("photos", exist_ok=True)
        
        try:
            await bot.download(photo, destination=file_path)
            photos.append(file_path)
        except Exception as e:
            await message.answer("Произошла ошибка при загрузке фотографии. Попробуйте ещё раз.")
            return
    else:
        await message.answer("Пожалуйста, отправьте фотографию или нажмите 'Пропустить'.")
        return

    await state.update_data(photos=photos)
    await state.set_state(CleaningFSM.floor_2_corridor)
    await message.answer(
        "📸 Отправьте фотографию коридора 2 этажа. При необходимости нажмите Пропустить.",
        reply_markup=skip_keyboard(),
    )

@dp.message(CleaningFSM.floor_2_corridor)
async def location_1_f2c(message: types.Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    photos = data.get("photos", [])

    if message.content_type == 'text' and message.text == "Пропустить":
        photos.append('skip')
    elif message.content_type == 'photo':
        photo = message.photo[-1]
        file_path = f"photos/{message.from_user.id}_location_1_{int(time.time())}.jpg"
        
        os.makedirs("photos", exist_ok=True)
        
        try:
            await bot.download(photo, destination=file_path)
            photos.append(file_path)
        except Exception as e:
            await message.answer("Произошла ошибка при загрузке фотографии. Попробуйте ещё раз.")
            return
    else:
        await message.answer("Пожалуйста, отправьте фотографию или нажмите 'Пропустить'.")
        return

    await state.update_data(photos=photos)
    await state.set_state(CleaningFSM.floor_2_restroom)
    await message.answer(
        "📸 Отправьте фотографию санузла 2 этажа. При необходимости нажмите Пропустить.",
        reply_markup=skip_keyboard(),
    )

@dp.message(CleaningFSM.floor_2_restroom)
async def location_1_f2r(message: types.Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    photos = data.get("photos", [])

    if message.content_type == 'text' and message.text == "Пропустить":
        photos.append('skip')
    elif message.content_type == 'photo':
        photo = message.photo[-1]
        file_path = f"photos/{message.from_user.id}_location_1_{int(time.time())}.jpg"
        
        os.makedirs("photos", exist_ok=True)
        
        try:
            await bot.download(photo, destination=file_path)
            photos.append(file_path)
        except Exception as e:
            await message.answer("Произошла ошибка при загрузке фотографии. Попробуйте ещё раз.")
            return
    else:
        await message.answer("Пожалуйста, отправьте фотографию или нажмите 'Пропустить'.")
        return

    await state.update_data(photos=photos)
    await state.set_state(CleaningFSM.stairsl1)
    await message.answer(
        "📸 Отправьте фотографию лестницы. При необходимости нажмите Пропустить.",
        reply_markup=skip_keyboard(),
    )

@dp.message(CleaningFSM.stairsl1)
async def location_1_st(message: types.Message, state: FSMContext, bot: Bot):
    
    data = await state.get_data()
    photos = data.get("photos", [])

    if message.content_type == 'text' and message.text == "Пропустить":
        photos.append('skip')
    elif message.content_type == 'photo':
        photo = message.photo[-1]
        file_path = f"photos/{message.from_user.id}_location_1_{int(time.time())}.jpg"
        
        os.makedirs("photos", exist_ok=True)
        
        try:
            await bot.download(photo, destination=file_path)
            photos.append(file_path)
        except Exception as e:
            await message.answer("Произошла ошибка при загрузке фотографии. Попробуйте ещё раз.")
            return
    else:
        await message.answer("Пожалуйста, отправьте фотографию или нажмите 'Пропустить'.")
        return

    await state.update_data(photos=photos)
    await state.set_state(CleaningFSM.additional_photo)
    await message.answer(
        "📸 Отправьте дополнительные фотографии если нужно. При необходимости нажмите Пропустить.",
        reply_markup=skip_keyboard(),
    )



#ВТОРОЙ АДРЕС
@dp.message(CleaningFSM.room_1)
async def location_2_r1(message: types.Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    photos = data.get("photos", [])

    if message.content_type == 'text' and message.text == "Пропустить":
        photos.append('skip')
    elif message.content_type == 'photo':
        photo = message.photo[-1]
        file_path = f"photos/{message.from_user.id}_location_2_{int(time.time())}.jpg"
        
        os.makedirs("photos", exist_ok=True)
        
        try:
            await bot.download(photo, destination=file_path)
            photos.append(file_path)
        except Exception as e:
            await message.answer("Произошла ошибка при загрузке фотографии. Попробуйте ещё раз.")
            return
    else:
        await message.answer("Пожалуйста, отправьте фотографию или нажмите 'Пропустить'.")
        return

    await state.update_data(photos=photos)
    await state.set_state(CleaningFSM.room_6)
    await message.answer(
        "📸 Отправьте фотографию комнаты №6. При необходимости нажмите Пропустить.",
        reply_markup=skip_keyboard(),
    )

@dp.message(CleaningFSM.room_6)
async def location_2_r6(message: types.Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    photos = data.get("photos", [])

    if message.content_type == 'text' and message.text == "Пропустить":
        photos.append('skip')
    elif message.content_type == 'photo':
        photo = message.photo[-1]
        file_path = f"photos/{message.from_user.id}_location_2_{int(time.time())}.jpg"
        
        os.makedirs("photos", exist_ok=True)
        
        try:
            await bot.download(photo, destination=file_path)
            photos.append(file_path)
        except Exception as e:
            await message.answer("Произошла ошибка при загрузке фотографии. Попробуйте ещё раз.")
            return
    else:
        await message.answer("Пожалуйста, отправьте фотографию или нажмите 'Пропустить'.")
        return

    await state.update_data(photos=photos)
    await state.set_state(CleaningFSM.restroom)
    await message.answer(
        "📸 Отправьте фотографию санузла. При необходимости нажмите Пропустить.",
        reply_markup=skip_keyboard(),
    )

@dp.message(CleaningFSM.restroom)
async def location_2_rr(message: types.Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    photos = data.get("photos", [])

    if message.content_type == 'text' and message.text == "Пропустить":
        photos.append('skip')
    elif message.content_type == 'photo':
        photo = message.photo[-1]
        file_path = f"photos/{message.from_user.id}_location_2_{int(time.time())}.jpg"
        
        os.makedirs("photos", exist_ok=True)
        
        try:
            await bot.download(photo, destination=file_path)
            photos.append(file_path)
        except Exception as e:
            await message.answer("Произошла ошибка при загрузке фотографии. Попробуйте ещё раз.")
            return
    else:
        await message.answer("Пожалуйста, отправьте фотографию или нажмите 'Пропустить'.")
        return

    await state.update_data(photos=photos)
    await state.set_state(CleaningFSM.stairsl2)
    await message.answer(
        "📸 Отправьте фотографию лестницы. При необходимости нажмите Пропустить.",
        reply_markup=skip_keyboard(),
    )

@dp.message(CleaningFSM.stairsl2)
async def location_2_st(message: types.Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    photos = data.get("photos", [])

    if message.content_type == 'text' and message.text == "Пропустить":
        photos.append('skip')
    elif message.content_type == 'photo':
        photo = message.photo[-1]
        file_path = f"photos/{message.from_user.id}_location_2_{int(time.time())}.jpg"
        
        os.makedirs("photos", exist_ok=True)
        
        try:
            await bot.download(photo, destination=file_path)
            photos.append(file_path)
        except Exception as e:
            await message.answer("Произошла ошибка при загрузке фотографии. Попробуйте ещё раз.")
            return
    else:
        await message.answer("Пожалуйста, отправьте фотографию или нажмите 'Пропустить'.")
        return

    await state.update_data(photos=photos)
    await state.set_state(CleaningFSM.corridor)
    await message.answer(
        "📸 Отправьте фотографию коридора. При необходимости нажмите Пропустить.",
        reply_markup=skip_keyboard(),
    )

@dp.message(CleaningFSM.corridor)
async def location_2_r1(message: types.Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    photos = data.get("photos", [])

    if message.content_type == 'text' and message.text == "Пропустить":
        photos.append('skip')
    elif message.content_type == 'photo':
        photo = message.photo[-1]
        file_path = f"photos/{message.from_user.id}_location_2_{int(time.time())}.jpg"
        
        os.makedirs("photos", exist_ok=True)
        
        try:
            await bot.download(photo, destination=file_path)
            photos.append(file_path)
        except Exception as e:
            await message.answer("Произошла ошибка при загрузке фотографии. Попробуйте ещё раз.")
            return
    else:
        await message.answer("Пожалуйста, отправьте фотографию или нажмите 'Пропустить'.")
        return

    await state.update_data(photos=photos)
    await state.set_state(CleaningFSM.additional_photo)
    await message.answer(
        "📸 Отправьте дополнительные фотографии если нужно. При необходимости нажмите Пропустить.",
        reply_markup=skip_keyboard(),
    )


@dp.message(CleaningFSM.additional_photo)
async def additional_photo_handler(message: types.Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    add_photos = data.get("add_photos", [])

    if message.content_type == 'text' and message.text == "Пропустить":
        add_photos.append('skip')
        await state.update_data(add_photos=add_photos)
        await state.set_state(CleaningFSM.consumabels)
        await message.answer(
        "Спасибо, теперь укажите какие расходники вы использовали, если такие есть",
        reply_markup=consumables_keyboard(),
    )
    elif message.content_type == 'photo':
        photo = message.photo[-1]
        file_path = f"photos/{message.from_user.id}_additional_{int(time.time())}.jpg"
        
        os.makedirs("photos", exist_ok=True)
        
        try:
            await bot.download(photo, destination=file_path)
            add_photos.append(file_path)
            await state.update_data(add_photos=add_photos)
            await message.answer(
                "Отправьте еще одну фотографию или нажмите Пропустить",
                reply_markup=skip_keyboard(),
            )
        except Exception as e:
            await message.answer("Произошла ошибка при загрузке фотографии. Попробуйте ещё раз.")
            return
    else:
        await message.answer("Пожалуйста, отправьте фотографию или нажмите 'Пропустить'.")
        return

   


#РАСХОДНИКИ
@dp.message(CleaningFSM.consumabels)
async def handle_consumabels_choose(message: types.Message, state: FSMContext):
    consumable = message.text
    data = await state.get_data()
    consumables = data.get("consumables", [])

    if consumable == 'Далее':
        await state.update_data(consumables = consumables)
        await state.set_state(CleaningFSM.order)
        await message.answer("Отлично. Теперь укажите какие расходники необходимо закупить", reply_markup=order_keyboard())
    else:
        if consumable in consumables:
            consumables.remove(consumable)
            await state.update_data(consumables = consumables)
            await message.answer("вы выбрали следующие расходники: " + format_strings_as_column(consumables) + "Желаете выбрать еще? Чтобы удалить расходник из выбранных нажмите на него еще раз", reply_markup=consumables_keyboard())
        else:
            consumables.append(consumable)
            await state.update_data(consumables = consumables)
            await message.answer("вы выбрали следующие расходники: " + format_strings_as_column(consumables) + "Желаете выбрать еще? Чтобы удалить расходник из выбранных нажмите на него еще раз", reply_markup=consumables_keyboard())          


#ЗАКАЗАТЬ
@dp.message(CleaningFSM.order)
async def handle_order_selection(message: types.Message, state: FSMContext):
    to_order = message.text
    data = await state.get_data()
    order = data.get("order", {}) 

    if to_order == 'Далее':
        await state.update_data(order=order)
        await state.set_state(CleaningFSM.toRepair)
        await message.answer(
            "Отлично. Теперь, пожалуйста, укажите, какие поломки были обнаружены, если такие имеются.",
            reply_markup=fixes_keyboard()
        )
    else:
        if to_order in order:
            print(str(data) + "\n 463 \n")
            del order[to_order]
            await state.update_data(order=order)
            print(str(data) + "\n 466 \n")

            order_list = "\n".join([f"{item}: {quantity}" for item, quantity in order.items()])
            await message.answer(
                f"Вы выбрали следующие расходники:\n{order_list}\n\nЖелаете выбрать еще? Чтобы удалить расходник из выбранных, нажмите на него еще раз.",
                reply_markup=order_keyboard()
            )

        else:
            order[to_order] = None  
            await state.update_data(order=order)
            await state.update_data(current_order = to_order)
            print(str(data) + "\n 477 \n")
            await state.set_state(CleaningFSM.order_amount)
            await message.answer(
                f"Укажите количество для расходника '{to_order}', пожалуйста, введите число.",
                reply_markup=None 
            )

@dp.message(CleaningFSM.order_amount)
async def handle_order_amount(message: types.Message, state: FSMContext):
    amount_text = message.text
    if not amount_text.isdigit():
        await message.answer("Пожалуйста, введите корректное число для количества расходника.")
        return

    amount = int(amount_text)
    data = await state.get_data()
    current_order = data.get("current_order")
    print(str(data) + "\n 495 \n")
    order = data.get("order", {})

    order[current_order] = amount
    await state.update_data(order=order)

    await state.set_state(CleaningFSM.order)

    order_list = "\n".join([f"{item}: {quantity}" for item, quantity in order.items()])
    await message.answer(
        f"Вы выбрали следующие расходники:\n{order_list}\n\nКакие еще расходники необходимо закупить, если такие имеются?",
        reply_markup=order_keyboard()
    )

 

#ПОЛОМКИ
@dp.message(CleaningFSM.toRepair)
async def handle_fixes_choose(message: types.Message, state: FSMContext):
    toRepair = message.text
    data = await state.get_data()
    repair = data.get("repair", {})
    if toRepair == 'Далее':
        await state.update_data(repair=repair)
        await state.set_state(CleaningFSM.final)
        await message.answer(
            "Отлично. На этом все.",
            reply_markup=final_keyboard()
        )
    else:
        if toRepair in repair:
            del repair[toRepair]
            await state.update_data(repair=repair)
            if repair:
                order_list = "\n".join([f"{key}: {'Фото добавлено' if value else 'Без фото'}" for key, value in repair.items()])
                await message.answer(
                    f"Вы указали следующие поломки:\n{order_list}\n\nЖелаете выбрать еще?",
                    reply_markup=fixes_keyboard()
                )
            else:
                await message.answer(
                    "Пожалуйста, укажите поломку из списка.",
                    reply_markup=fixes_keyboard()
                )
        else:
            repair[toRepair] = None  
            await state.update_data(repair=repair)
            await state.update_data(toRepair = toRepair)
            await state.set_state(CleaningFSM.repair_photo)
            await message.answer(
                f"Пожалуйста, отправьте фотографию поломки '{toRepair}'.",
                reply_markup=None 
            )
             
@dp.message(CleaningFSM.repair_photo)
async def handle_fix_photo(message: types.Message, state: FSMContext, bot:Bot):
    data = await state.get_data()
    repair = data.get("repair", {})
    toRepair = data.get('toRepair')

    photo = message.photo[-1]
    file_path = f"photos/{message.from_user.id}_repair_{int(time.time())}.jpg"
        
    os.makedirs("photos", exist_ok=True)
        
    try:
        await bot.download(photo, destination=file_path)
        repair[toRepair] = file_path
    except Exception as e:
        await message.answer("Произошла ошибка при загрузке фотографии. Попробуйте ещё раз.")
        return

    await state.update_data(repair=repair)
    await state.set_state(CleaningFSM.toRepair)
    await message.answer(
        "Пожалуйста, выбирете еще поломки, если таковые имеються",
        reply_markup=fixes_keyboard(),
    )
              



@dp.message(CleaningFSM.final)
async def handle_consumabels_choose(message: types.Message, state: FSMContext):
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    await state.update_data(finishTime = formatted_datetime)
    data = await state.get_data()
    print(str(data))
    t_id = message.from_user.id
    user = await db_manager.get_user_by_telegram_id(t_id)
    phone = user['phone_number']
    print(phone)


    await db_manager.add_task(
    str(phone),
    str(t_id), 
    data.get('chosen_building', ""), 
    json.dumps(data.get('photos', [])), 
    json.dumps(data.get('add_photos', [])),  
    json.dumps(data.get('consumables', [])),  
    json.dumps(data.get('order', {})), 
    json.dumps(data.get('repair', {})),  
    data.get('startTime', ""), 
    data.get('finishTime', ""),  
    True
)



    await message.answer("Спасибо что выбираете нас!", reply_markup=start_cleaning_button())
    await state.clear() 


async def main():
    await db_manager.initialize()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())