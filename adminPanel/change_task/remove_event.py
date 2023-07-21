from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from states.admin_panel import FormChangeTasks, FormRemoveEvent

from keyboards import Keyboards, kb_types_events, kb_events


async def start_form_removeEvent(message: types.Message):
    await FormRemoveEvent.select_type.set()
    await message.answer("Открыта форма удаления задач", reply_markup=Keyboards.empty_method)

    await message.answer("Укажите, по какому типу хотите посмотреть задачи", reply_markup=await kb_types_events())


async def process_select_type(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['select_type'] = callback_query.data
    await FormRemoveEvent.next()
    bot = callback_query.bot
    await bot.edit_message_text(
        text="Выберите задачу, которую нужно удалить:",
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id,
        reply_markup=await kb_events(callback_query.data),
        parse_mode="Markdown"
    )


def register_handlers_remove_event(dp: Dispatcher):
    dp.register_message_handler(start_form_removeEvent,
                                content_types=['text'],
                                text='Удалить задачу',
                                state=FormChangeTasks.menu)

    dp.register_callback_query_handler(process_select_type,
                                       lambda c: c.data.isdigit(),
                                       state=FormRemoveEvent.select_type)