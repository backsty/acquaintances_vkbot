from vk_api.keyboard import VkKeyboard, VkKeyboardColor


class Button:
    def __init__(self):
        pass

    def start(self) -> VkKeyboard.get_keyboard:
        start_key = VkKeyboard(inline=False,
                               one_time=True)  # one_time: Если True, клавиатура исчезнет после нажатия на кнопку

        start_key.add_button("Начать поиск", color=VkKeyboardColor.POSITIVE)
        start_key.add_button("Вернуться к поиску", color=VkKeyboardColor.POSITIVE)
        start_key.add_line()
        start_key.add_button("Показать понравившиеся фото", color=VkKeyboardColor.POSITIVE)
        start_key.add_line()
        start_key.add_button("Показать чёрный список", color=VkKeyboardColor.PRIMARY)
        start_key.add_line()
        start_key.add_button("Показать список избранных", color=VkKeyboardColor.PRIMARY)
        return start_key.get_keyboard()

    def next(self) -> VkKeyboard.get_keyboard:
        next_key = VkKeyboard(inline=False,
                              one_time=True)  # one_time: Если True, клавиатура исчезнет после нажатия на кнопку

        next_key.add_button("Далее", color=VkKeyboardColor.PRIMARY)
        next_key.add_button("Начать сначала", color=VkKeyboardColor.PRIMARY)
        next_key.add_line()
        next_key.add_button("Добавить в чёрный список", color=VkKeyboardColor.NEGATIVE)
        next_key.add_line()
        next_key.add_button("Добавить в избранные", color=VkKeyboardColor.PRIMARY)
        next_key.add_button("В главное меню", color=VkKeyboardColor.PRIMARY)
        return next_key.get_keyboard()

    def delete_blocklist(self) -> VkKeyboard.get_keyboard:
        delete_blocklist = VkKeyboard(inline=False,
                                      one_time=True)  # one_time: Если True, клавиатура исчезнет после нажатия на кнопку

        delete_blocklist.add_button("Удалить из чёрного списка", color=VkKeyboardColor.NEGATIVE)
        delete_blocklist.add_button("В главное меню", color=VkKeyboardColor.PRIMARY)
        return delete_blocklist.get_keyboard()

    def yes_or_no(self) -> VkKeyboard.get_keyboard:
        yes_or_no = VkKeyboard(inline=False,
                               one_time=True)  # one_time: Если True, клавиатура исчезнет после нажатия на кнопку

        yes_or_no.add_button("Удалить все данные", color=VkKeyboardColor.NEGATIVE)
        yes_or_no.add_button("Нет я передумал", color=VkKeyboardColor.PRIMARY)
        return yes_or_no.get_keyboard()

    def delete_photo(self) -> VkKeyboard.get_keyboard:
        delete_photo = VkKeyboard(inline=False,
                                      one_time=True)  # one_time: Если True, клавиатура исчезнет после нажатия на кнопку

        delete_photo.add_button("Удалить фото из понравившихся", color=VkKeyboardColor.NEGATIVE)
        delete_photo.add_button("В главное меню", color=VkKeyboardColor.PRIMARY)
        return delete_photo.get_keyboard()

    def delete_favourite(self) -> VkKeyboard.get_keyboard:
        delete_favourite = VkKeyboard(inline=False,
                                  one_time=True)  # one_time: Если True, клавиатура исчезнет после нажатия на кнопку

        delete_favourite.add_button("Удалить фото из избранных", color=VkKeyboardColor.NEGATIVE)
        delete_favourite.add_button("В главное меню", color=VkKeyboardColor.PRIMARY)
        return delete_favourite.get_keyboard()

    def back_to_menu(self) -> VkKeyboard.get_keyboard:
        back_to_menu = VkKeyboard(inline=False,
                                      one_time=True)  # one_time: Если True, клавиатура исчезнет после нажатия на кнопку

        back_to_menu.add_button("В главное меню", color=VkKeyboardColor.PRIMARY)
        return back_to_menu.get_keyboard()

    def like_or_dislike(self) -> VkKeyboard.get_keyboard:
        like_or_dislike = VkKeyboard(inline=False,
                                  one_time=True)  # one_time: Если True, клавиатура исчезнет после нажатия на кнопку

        like_or_dislike.add_button("Like", color=VkKeyboardColor.POSITIVE)
        like_or_dislike.add_button("Dislike", color=VkKeyboardColor.NEGATIVE)
        return like_or_dislike.get_keyboard()
