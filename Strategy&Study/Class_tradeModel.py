Init signature: trade.Model(self, *args)
Source:        
class Model(sdk.TradingModel):
    def on_market_data_update(self, data):
        import sdk
        if data.type == "Snapshot" :
            self.on_data_update(sdk.Snapshot_from_market_data(data))
        else:
            self.on_data_update(sdk.Bar_from_market_data(data))

    def on_order_status_update(self, order):
        import sdk
        if order.order_type == "FUTURES" :
            self.on_order_update(FuturesOrder(sdk.FuturesOrder_from_order_basis(order)))
        elif order.order_type == "STOCK" :
            self.on_order_update(StockOrder(sdk.StockOrder_from_order_basis(order)))
        elif order.order_type == "TWAP_STOCK":
            self.on_order_update(TwapStockOrder(sdk.TwapStockOrder_from_order_basis(order)))

    def place_future_order(self, symbol, signed_size, price,
                           position_effect=PositionEffect.SMART,
                           duration=Duration.EOD,
                           hedge_effect=HedgeEffect.SPECULATION,
                           deal_account_id="",
                           gate_type=""):
        """ Place a futures order. SUCCESS will be returned when the order is sent to
        ... the broker; otherwise, the rejection reason will be returned.
        @param symbol: name of the instrument
        @type symbol: string
        @param signed_size: Positive for a buying order and negative for a
        ... selling one. It cannot be zero.
        @type signed_size: long
        @param price: A specific number for a limit order or number of levels
        ... of matching for a market order.
        @type price: float or MarketPrice
        @param duration: EOD(end-of-day), FOK(fill-or-kill) or FAK(fill-and-kill).
        @type duration: int
        @param position_effect: OPEN, COVER or COVER_TODAY.
        @type position_effect: int
        @param hedge_effect: SPECULATION, HEDGE or ARBITRAGE
        @type hedge_effect: int
        @param deal_account_id:
        @type deal_account_id: string
        @param gate_type: CTP or TradeStation
        @type gate_type: string
        @rtype: int
        """
        if type(price) != MarketPrice:
            from sdk import LIMIT
            return super(Model, self).place_future_order(symbol, signed_size, price, LIMIT,
                                                         position_effect, duration, hedge_effect,
                                                         deal_account_id, gate_type)
        else:
            return super(Model, self).place_future_order(symbol, signed_size, 0.0, price.__to_enum__(),
                                                         position_effect, duration, hedge_effect,
                                                         deal_account_id, gate_type)

    def place_stock_order(self, symbol, signed_size,
                          price, duration=Duration.EOD,
                          deal_account_id='', gate_type=''):
        """ Place a stock order. SUCCESS will be returned when the order is sent to
        ... the broker; otherwise, the rejection reason will be returned.
        @param symbol: it's the security name
        @type symbol: string
        @param signed_size: Positive for a buying order and negative for a
        ... selling one. It cannot be zero.
        @type signed_size: long
        @param price: A specific number for a limit order or number of levels
        ... of matching for a market order.
        @type price: float or MarketPrice
        @param duration: EOD(end-of-day), FOK(fill-or-kill) or FAK(fill-and-kill).
        @type duration: int
        @param deal_account_id:
        @type deal_account_id: string
        @param gate_type: CTP or TradeStation
        @type gate_type: string
        @rtype int
        """
        if type(price) != MarketPrice:
            from sdk import LIMIT
            return super(Model, self).place_stock_order(symbol, signed_size,
                                                        price, LIMIT, duration,
                                                        deal_account_id, gate_type)
        else:
            return super(Model, self).place_stock_order(symbol, signed_size,
                                                        0.0, price.__to_enum__(),
                                                        duration, deal_account_id,
                                                        gate_type)

    def place_twap_stock_order(self, symbol, signed_size, price, time_length, times,
                               duration=Duration.EOD, deal_account_id='', gate_type=''):
        if type(price) != MarketPrice:
            from sdk import LIMIT
            return super(Model, self).place_twap_stock_order(symbol, signed_size,
                                                             price, LIMIT, time_length,
                                                             times, duration,
                                                             deal_account_id, gate_type)
        else:
            return super(Model, self).place_twap_stock_order(symbol, signed_size,
                                                             0.0, price.__to_enum__(),
                                                             time_length, times,
                                                             duration, deal_account_id,
                                                             gate_type)
    def cancel_twap_stock_order(self, order_id):
        return super(Model, self).cancel_twap_stock_order(order_id)


    def place_chase_stock_order(self, symbol, signed_size, price, time_interval, times,
                               duration=Duration.EOD, deal_account_id='', gate_type=''):
        if type(price) != MarketPrice:
            from sdk import LIMIT
            return super(Model, self).place_twap_stock_order(symbol, signed_size,
                                                             price, LIMIT, time_interval, times,
                                                             duration,deal_account_id, gate_type)
        else:
            return super(Model, self).place_twap_stock_order(symbol, signed_size,
                                                             0.0, price.__to_enum__(),
                                                             time_interval, times,
                                                             duration, deal_account_id,
                                                             gate_type)
    def cancel_chase_stock_order(self, order_id):
        return super(Model, self).cancel_chase_stock_order(order_id)

    def get_order(self, order_id):
        """ Retrieve an order with order_id. If order_id is invalid or the state of 
        ... the order has been FINAL, None will be returned.
        @type order_id: id of the order.
        @rtype: FuturesOrder or StockOrder or None
        """
        sself = super(Model, self)
        return FuturesOrder(sself.get_futures_order(order_id)) \
            or StockOrder(sself.get_stock_order(order_id)) \
            or TwapStockOrder(sself.get_twap_stock_order(order_id)) or None

    def cancel_future_order(self, order_id):
        """Cancel a futures order with order_id. If cancellation of the order is sent
        ... to the broker, True will be returned.
        @type order_id: id of the order.
        @rtype: bool
        """
        return super(Model, self).cancel_future_order(order_id)

    def cancel_stock_order(self, order_id):
        """Cancel a stock order with order_id. If cancellation of the order is sent
        ... to the broker, True will be returned.
        @type order_id: id of the order.
        @rtype: bool
        """
        return super(Model, self).cancel_stock_order(order_id)

    def on_order_update(self, order):
        """ Called when the state of an order is updated.
        @type order: Order
        """
        raise ValueError("You must define a 'on_order_update' function.")

    def on_data_update(self, data):
        """ Called when a subscribed market data arrives.
        @param data: the subscribed market data.
        @type data: Bar or Snapshot
        """
        raise ValueError("You must define a 'on_data_update' function.")

    def on_initialize(self):
        """ Initialization of the strategy.
        """
        raise ValueError("You must define a 'on_initialize' function.")

    def get_current_time(self):
        """ Retrieve the current trading time in UTC microseconds        
        @rtype: long
        """
        return super(Model, self).get_current_time()

    def on_pause(self):
        """ Called when pause is requested.
        """
        pass

    def on_resume(self):
        """ Called when resume is requested.
        """
        pass

    def on_stop(self):
        """ Called when stop is requested.
        """
        pass

    def on_market_open(self, market):
        """
        Called when the market is opened
        """
        pass

    def on_market_close(self, market):
        """
        called when the market is closed
        """
        pass
File:           /opt/local/lib/python2.7/site-packages/Mustang-20161031-py2.7.egg/quant/trade.py
Type:           type