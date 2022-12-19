from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        """Получить строку сообщения о тренировке."""
        output = (
            f"Тип тренировки: {self.training_type}; "
                                             f"Длительность: {self.duration:.3f} ч.; "
            f"Дистанция: {self.distance:.3f} км; "
            f"Ср. скорость: {self.speed:.3f} км/ч; "
            f"Потрачено ккал: {self.calories:.3f}."
        )
        return output


@dataclass
class Training:
    """Базовый класс тренировки."""

    LEN_STEP = 0.65
    M_IN_KM = 1000

    action: int
    duration: float
    weight: float

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed = self.get_distance() / self.duration
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            type(self).__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories(),
        )


class Running(Training):
    """Тренировка: бег."""

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        COEFF_CALORIE_1 = 18
        COEFF_CALORIE_2 = 20
        calories = (
            (COEFF_CALORIE_1 * self.get_mean_speed() - COEFF_CALORIE_2)
            * self.weight
            / self.M_IN_KM
            * (self.duration * 60)
        )
        return calories


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    height: float

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        COEFF_CALORIE_1 = 0.035
        COEFF_CALORIE_2 = 0.029
        calories = (
            COEFF_CALORIE_1 * self.weight
            + (self.get_mean_speed() ** 2 // self.height)
            * COEFF_CALORIE_2
            * self.weight
        ) * (self.duration * 60)
        return calories


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP = 1.38

    length_pool: int
    count_pool: int

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed = (
            self.length_pool * self.count_pool / self.M_IN_KM / self.duration
        )
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        COEFF_CALORIE_1 = 1.1
        COEFF_CALORIE_2 = 2
        calories = (
            (self.get_mean_speed() + COEFF_CALORIE_1)
            * COEFF_CALORIE_2
            * self.weight
        )
        return calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout = {"SWM": Swimming, "RUN": Running, "WLK": SportsWalking}

    for key in workout.keys():
        if workout_type == key:
            constr = workout[key]
            return constr(*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == "__main__":
    packages = [
        ("SWM", [720, 1, 80, 25, 40]),
        ("RUN", [15000, 1, 75]),
        ("WLK", [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
