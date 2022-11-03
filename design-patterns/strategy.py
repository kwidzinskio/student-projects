'''

We want to transport a certain item from A to B. We have the following means of transport, each with a specific cost,
travel time and risk of losing / damaging the item:

Bike (cost: PLN 0, time: 60 minutes, risk: high)

Public transport (cost: PLN 3, duration: 30 minutes, risk: medium)

Taxi (cost: PLN 20, duration: 15 minutes, risk: small)

We have a certain amount of money and time at our disposal as well as the value of the item (entered from the keyboard).
On this basis, implement (in python or C ++ or ...) the choice of means of transport to transport the object, using the
design pattern Strategy.
'''
import enum


class Risk(enum.Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3


class Context:
    def __init__(self, strategy):
        self._strategy = strategy

    def run(self, *args, **kwargs):
        return self._strategy.is_applicable(*args, **kwargs)


class Strategy():
    _required_fields = ['cost', 'risk', 'time']
    cost, risk, time = None, None, None

    def __init__(self):
        if not all(getattr(self, field, None) is not None for field in self._required_fields):
            raise NotImplementedError(f'You need to specify all of: {self._required_fields}')

    def is_applicable(self, money: float, time: float, risk: Risk):
        if money < self.cost:
            return

        if time < self.time:
            return

        if risk.value < self.risk.value:
            return

        return True


class TaxiStrategy(Strategy):
    cost = 20
    risk = Risk.LOW
    time = 15


class BikeStrategy(Strategy):
    cost = 0
    risk = Risk.HIGH
    time = 60


class PublicTransportStrategy(Strategy):
    cost = 3
    risk = Risk.MEDIUM
    time = 30


if __name__ == '__main__':
    print('Input available funds: ')

    while True:
        try:
            money = float(input())
            if money < 0:
                raise ValueError('You have to provide positive value')
            break
        except ValueError as exc:
            print(exc)

    print('Input available time: ')

    while True:
        try:
            time = float(input())
            if time < 0:
                raise ValueError('You have to provide positive value')
            break
        except ValueError as exc:
            print(exc)

    print('Input risk indicator: ')
    print('Choices: ' + str({r.name: r.value for r in Risk}))

    while True:
        try:
            risk = int(input())
            risk = Risk(risk)
            break
        except ValueError as exc:
            print(exc)

    strategies = [BikeStrategy, TaxiStrategy, PublicTransportStrategy]
    applicable_strategies = []
    non_applicable_strategies = []

    for S in strategies:
        context = Context(S())
        if context.run(money=money, time=time, risk=risk):
            applicable_strategies.append(S)
        else:
            non_applicable_strategies.append(S)

    print(f'Providing:\n funds: {money}\n time: {time}\n risk indicatior: {risk}\n'
          f'available strategies: {applicable_strategies}, whereas strategies {non_applicable_strategies} has been rejected.')
