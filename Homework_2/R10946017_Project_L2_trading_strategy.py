class Strategy():
    # option setting needed
    def __setitem__(self, key, value):
        self.options[key] = value

    # option setting needed
    def __getitem__(self, key):
        return self.options.get(key, '')

    def __init__(self):
        # strategy property
        self.subscribedBooks = {
            'Bitfinex': {
                'pairs': ['BTC-USDT'],
            },
        }
        self.period = 2 * 60 * 60
        self.options = {}

        # user defined class attribute
        self.price_log = np.array([])
        self.bought_price_log = np.array([])

    # 回傳每一筆訂單記錄
    def on_order_state_change(self, order):
        Log("on order state change message: " + str(order) + " order price: " + str(order["price"]))

    # called every self.period
    def trade(self, information):
        # 決定使用的 exchange 交易所
        exchange = list(information['candles'])[0]
        # 決定使用的 pair (e.g. BTC-USDT)
        pair = list(information['candles'][exchange])[0]
        target_currency = pair.split('-')[0]  # ETH
        base_currency = pair.split('-')[1]  # USDT
        base_currency_amount = self['assets'][exchange][base_currency]
        target_currency_amount = self['assets'][exchange][target_currency]

        high = information['candles'][exchange][pair][0]['high']
        low = information['candles'][exchange][pair][0]['open']
        mean = (low + high) / 2
        # Log("(high+low)/2" +str(mean))
        self.price_log = np.append(self.price_log, [float(mean)])
        # Log(str(self.price_log))
        # Log(str(information['candles'][exchange][pair][0]['time']))

        Given_String = information['candles'][exchange][pair][0]['time']
        year = int(Given_String.split('-')[0])
        month = int(Given_String.split('-')[1])
        date = Given_String.split('-')[2]

        time = date.split('T')[1]
        date = int(date.split('T')[0])

        hour = int(time.split(':')[0])
        minute = int(time.split(':')[1])
        # Log(str(year)+" "+str(month)+" "+str(date)+" "+str(hour)+" "+str(minute))
        if ((year == 2021) & (month == 11) & (date >= 8) & (hour >= 12) & (minute >= 0)):
            Log(str(information['candles'][exchange][pair][0]['time']))
            Log("===== Sell All! ===== ")
            return [
                {
                    'exchange': exchange,
                    'amount': -target_currency_amount,
                    'price': -1,
                    'type': 'MARKET',
                    'pair': pair,
                }
            ]

        else:
            # Log(str(information['candles'][exchange][pair][0]['time']))
            if mean < 0.85 * information['candles'][exchange][pair][0]['close']:
                return [
                    {
                        'exchange': exchange,
                        'amount': -target_currency_amount,
                        'price': -1,
                        'type': 'MARKET',
                        'pair': pair,
                    }
                ]
            elif mean > max(self.price_log[-5:-2]) > max(self.bought_price_log[-5:-1]):
                return [
                    {
                        'exchange': exchange,
                        'amount': -target_currency_amount,
                        'price': -1,
                        'type': 'MARKET',
                        'pair': pair,
                    }
                ]

            elif mean < min(self.price_log[-30:-2]):
                self.bought_price_log = np.append(self.bought_price_log, [float(mean)])
                return [
                    {
                        'exchange': exchange,
                        'amount': 1,
                        'price': -1,
                        'type': 'MARKET',
                        'pair': pair,
                    }
                ]

            else:
                pass

            return []