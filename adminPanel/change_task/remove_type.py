from aiogram import Dispatcher, types

from states.admin_panel import FormChangeTasks, FormRemoveTypeEvent

from keyboards import Keyboards, kb_types_events

from database.methods import db_remove_type


async def start_form_removeTypeEvent(message: types.Message):
    await FormRemoveTypeEvent.select_type.set()
    await message.answer("Открыта форма удаления типов", reply_markup=Keyboards.empty_method)

    await message.answer("⚠️\nВсе связанные с этим типом задачи будут удалены\n"
                         "\nУкажите, какой тип хотите удалить", reply_markup=await kb_types_events())


async def process_remove_type_event(callback_query: types.CallbackQuery):
    id_type = callback_query.data
    await db_remove_type(id_type)
    await callback_query.bot.edit_message_text(text="Удалено успешно",
                                               chat_id=callback_query.from_user.id,
                                               message_id=callback_query.message.message_id,
                                               reply_markup=await kb_types_events())


def register_handlers_remove_type_event(dp: Dispatcher):

    dp.register_message_handler(start_form_removeTypeEvent,
                                content_types=['text'],
                                text='Удалить тип задачи',
                                state=FormChangeTasks.menu)

    dp.register_callback_query_handler(process_remove_type_event,
                                       lambda c: c.data.isdigit(),
                                       state=FormRemoveTypeEvent.select_type)
    