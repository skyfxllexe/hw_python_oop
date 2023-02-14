class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self, training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self):
        if self.training_type == 'SWM':
            return (f'Тип тренировки: Swimming;\n'
                    f'Длительность: {float(self.duration):.3f} ч.;\n'
                    f'Дистанция: {float(self.distance):.3f} км;\n'
                    f'Ср. скорость: {float(self.speed):.3f} км/ч;\n'
                    f'Потрачено ккал: {float(self.calories):.3f}.\n')
        if self.training_type == 'RUN':
            return (f'Тип тренировки: Running;\n'
                    f'Длительность: {float(self.duration):.3f} ч.;\n'
                    f'Дистанция: {float(self.distance):.3f} км;\n'
                    f'Ср. скорость: {float(self.speed):.3f} км/ч;\n'
                    f'Потрачено ккал: {float(self.calories):.3f}.\n')
        return (f'Тип тренировки: SportsWalking;\n'
                f'Длительность: {float(self.duration):.3f} ч.;\n'
                f'Дистанция: {float(self.distance):.3f} км;\n'
                f'Ср. скорость: {float(self.speed):.3f} км/ч;\n'
                f'Потрачено ккал: {float(self.calories):.3f}.\n')


M_IN_KM: int = 1000


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    const: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return 0.0

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage("TR", self.duration, self.get_distance(),
                           self.get_mean_speed(), self.get_spent_calories()
                           )


class Running(Training):
    """Тренировка: бег."""
    cmf: int = 18
    cms: float = 1.79

    def __init__(self, action: float, duration: float, weight: float) -> None:
        super().__init__(action, duration, weight)
        self.LEN_STEP: float = 0.65

    def get_distance(self) -> float:
        return (self.action * self.LEN_STEP / M_IN_KM)

    def get_mean_speed(self) -> float:
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        cmf: int = 18
        cms: float = 1.79
        return ((cmf * self.get_mean_speed() + cms)
                * self.weight / M_IN_KM * self.duration * 60)

    def show_training_info(self) -> InfoMessage:
        return InfoMessage("RUN", self.duration, self.get_distance(),
                           self.get_mean_speed(), self.get_spent_calories()
                           )


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    cmf: float = 0.035
    cms: float = 0.029
    newconst: float = 0.278
    newconst2: int = 100

    def __init__(self,
                 action: float,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height
        self.LEN_STEP: float = 0.65

    def get_distance(self) -> float:
        return (self.action * self.LEN_STEP / M_IN_KM)

    def get_mean_speed(self) -> float:
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        cmf: float = 0.035
        cms: float = 0.029
        newconst: float = 0.278
        newconst2: int = 100
        avgspeed: float = (self.get_mean_speed() * newconst) ** 2
        return ((cmf * self.weight + (avgspeed / (self.height / newconst2))
                 * cms * self.weight) * self.duration * 60)

    def show_training_info(self) -> InfoMessage:
        return InfoMessage("WLK", self.duration, self.get_distance(),
                           self.get_mean_speed(), self.get_spent_calories()
                           )


class Swimming(Training):
    """Тренировка: плавание."""
    cmf: float = 1.1
    sm: int = 2
    LEN_STEP: float = 1.38

    def __init__(self,
                 action: float,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool
        self.LEN_STEP: float = 1.38

    def get_distance(self) -> float:
        return self.action * self.LEN_STEP / M_IN_KM

    def get_mean_speed(self) -> float:
        return self.length_pool * self.count_pool / M_IN_KM / self.duration

    def get_spent_calories(self) -> float:
        cmf: float = 1.1
        sm: int = 2
        return (self.get_mean_speed() + cmf) * sm * self.weight * self.duration

    def show_training_info(self) -> InfoMessage:
        return InfoMessage("SWM", self.duration, self.get_distance(),
                           self.get_mean_speed(), self.get_spent_calories()
                           )


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    if workout_type == 'SWM':
        return Swimming(data[0], data[1], data[2], data[3], data[4])
    if workout_type == 'RUN':
        return Running(data[0], data[1], data[2])
    return SportsWalking(data[0], data[1], data[2], data[3])


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
