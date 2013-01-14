from operator import (AnyQuery, BetweenQuery, ContainsQuery, EqualityQuery,
                      GreaterThanQuery, LessThanQuery)


class QueryFactory(object):
    """
    Collection Search Query Factories

    Example Usage::

        from myemma.query.factory import QueryFactory as q

        query1 = q.eq('member_field:foo', 1) & q.contains('member_field:bar', 2)
        "%s" % query1 # ["and", ["member_field:foo", "eq", 1], ["member_field:bar", "eq", 2]]

        query2 = q.eq('member_field:foo', 1) | q.contains('member_field:bar', 2)
        "%s" % query2 # ["or", ["member_field:foo", "eq", 1], ["member_field:bar", "eq", 2]]

        query3 = ~ q.eq('member_field:foo', 1)
        "%s" % query3 # ["not", ["member_field:foo", "eq", 1]]

    """
    @staticmethod
    def eq(field, value):
        """
        Equality Query Factory

        :param field: Field name to query
        :type field: :class:`str`
        :param value: Value to select
        :type value: :class:`str` or :class:`int`
        :rtype: :class:`CompositeQuery`

        Example Usage::

            from myemma.query.factory import QueryFactory as q

            query = q.eq('member_field:some_string_field', 'bar')
            "%s" % query # ["member_field:some_string_field", "eq", "bar"]

        """
        return EqualityQuery(field, value)
    @staticmethod
    def lt(field, value):
        """
        Less Than Query Factory

        :param field: Field name to query
        :type field: :class:`str`
        :param value: Value to select
        :type value: :class:`int`
        :rtype: :class:`CompositeQuery`

        Example Usage::

            from myemma.query.factory import QueryFactory as q

            query = q.lt('member_field:some_numeric_field', 10)
            "%s" % query # ["member_field:some_numeric_field", "lt", 10]

        """
        return LessThanQuery(field, value)
    @staticmethod
    def gt(field, value):
        """
        Greater Than Query Factory

        :param field: Field name to query
        :type field: :class:`str`
        :param value: Value to select
        :type value: :class:`int`
        :rtype: :class:`CompositeQuery`

        Example Usage::

            from myemma.query.factory import QueryFactory as q

            query = q.gt('member_field:some_numeric_field', 5)
            "%s" % query # ["member_field:some_numeric_field", "gt", 5]

        """
        return GreaterThanQuery(field, value)
    @staticmethod
    def between(field, low, high):
        """
        Between Query Factory

        :param field: Field name to query
        :type field: :class:`str`
        :param low: Min value to select
        :type low: :class:`int`
        :param high: Max value to select
        :type high: :class:`int`
        :rtype: :class:`CompositeQuery`

        Example Usage::

            from myemma.query.factory import QueryFactory as q

            query = q.between('member_field:some_numeric_field', 5, 10)
            "%s" % query # ["member_field:some_numeric_field", "between", 5, 10]

        """
        return BetweenQuery(field, low, high)
    @staticmethod
    def contains(field, value):
        """
        Contains Query Factory

        :param field: Field name to query
        :type field: :class:`str`
        :param value: Value to select
        :type value: :class:`str`
        :rtype: :class:`CompositeQuery`

        Example Usage::

            from myemma.query.factory import QueryFactory as q

            query = q.contains('member_field:some_string_field', '*foo*')
            "%s" % query # ["member_field:some_string_field", "contains", "*foo*"]

        """
        return ContainsQuery(field, value)
    @staticmethod
    def any(field, value):
        """
        Any Query Factory

        :param field: Field name to query
        :type field: :class:`str`
        :param value: Value to select
        :type value: :class:`str` or :class:`int`
        :rtype: :class:`CompositeQuery`

        Example Usage::

            from myemma.query.factory import QueryFactory as q

            query = q.any('member_field:some_array_field', 'ten')
            "%s" % query # ["member_field:some_array_field", "any", "ten"]

        """
        return AnyQuery(field, value)
