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

    def get_message(self) -> str:
        return str((f'Тип тренировки: {self.training_type}; '
                    f'Длительность: {float(self.duration):.3f} ч.; '
                    f'Дистанция: {float(self.distance):.3f} км; '
                    f'Ср. скорость: {float(self.speed):.3f} км/ч; '
                    f'Потрачено ккал: {float(self.calories):.3f}.'))


class Training:
    """Базовый класс тренировки."""
    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65
    CONST: int = 60
    METR_TO_SM: int = 100
    HOURINMIN: int = 60

    def __init__(self,
                 action: float,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action: float = action
        self.duration: float = duration
        self.weight: float = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration, self.get_distance(),
                           self.get_mean_speed(), self.get_spent_calories()
                           )


class Running(Training):
    """Тренировка: бег."""
    CMF: int = 18
    CMS: float = 1.79

    def get_spent_calories(self) -> float:
        return ((self.CMF * self.get_mean_speed() + self.CMS)
                * self.weight / self.M_IN_KM * self.duration * self.HOURINMIN)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CMF: float = 0.035
    CMS: float = 0.029
    METRPS: float = 0.278
    METR_TO_SM: int = 100

    def __init__(self,
                 action: float,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height: float = height

    def get_spent_calories(self) -> float:
        avgspeed: float = (self.get_mean_speed() * self.METRPS) ** 2
        return ((self.CMF * self.weight
                 + (avgspeed / (self.height / self.METR_TO_SM))
                 * self.CMS * self.weight) * self.duration * self.HOURINMIN)


class Swimming(Training):
    """Тренировка: плавание."""
    CMF: float = 1.1
    MULTITWO: int = 2
    LEN_STEP: float = 1.38

    def __init__(self,
                 action: float,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool: float = length_pool
        self.count_pool: int = count_pool

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed() + self.CMF)
                * self.MULTITWO * self.weight * self.duration)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    types = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if not (workout_type in types.keys()):
        raise Exception("Нет такой тренировки")
    return types[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
        ('NSW', [2, 3, 4, 1])
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
