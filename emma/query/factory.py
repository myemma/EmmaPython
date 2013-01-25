"""Search syntax builder"""

from emma.query import operator


class QueryFactory(object):
    """
    A collection of search query factories

    Usage::

        >>> qf = QueryFactory
        >>> query1 = qf.eq('member_field:foo', 1) & qf.contains('member_field:bar', '*foo*')
        >>> query1.to_tuple()
        ("and", ("member_field:foo", "eq", 1), ("member_field:bar", "contains", "*foo*"))

        >>> query2 = qf.eq('member_field:foo', 1) | qf.contains('member_field:bar', '*foo*')
        >>> query2.to_tuple()
        ("or", ("member_field:foo", "eq", 1), ("member_field:bar", "eq", "*foo*"))

        >>> query3 = ~ qf.eq('member_field:foo', 1)
        >>> query3.to_tuple()
        ("not", ("member_field:foo", "eq", 1))

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

        Usage::

            >>> from emma.query.factory import QueryFactory as qf
            >>> query = qf.eq('member_field:some_string_field', 'bar')
            >>> query.to_tuple()
            ("member_field:some_string_field", "eq", "bar")

        """
        return operator.EqualityQuery(field, value)

    @staticmethod
    def lt(field, value):
        """
        Less Than Query Factory

        :param field: Field name to query
        :type field: :class:`str`
        :param value: Value to select
        :type value: :class:`int`
        :rtype: :class:`CompositeQuery`

        Usage::

            >>> from emma.query.factory import QueryFactory as qf
            >>> query = qf.lt('member_field:some_numeric_field', 10)
            >>> query.to_tuple()
            ("member_field:some_numeric_field", "lt", 10)

        """
        return operator.LessThanQuery(field, value)

    @staticmethod
    def gt(field, value):
        """
        Greater Than Query Factory

        :param field: Field name to query
        :type field: :class:`str`
        :param value: Value to select
        :type value: :class:`int`
        :rtype: :class:`CompositeQuery`

        Usage::

            >>> from emma.query.factory import QueryFactory as qf
            >>> query = qf.gt('member_field:some_numeric_field', 5)
            >>> query.to_tuple()
            ("member_field:some_numeric_field", "gt", 5)

        """
        return operator.GreaterThanQuery(field, value)

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

        Usage::

            >>> from emma.query.factory import QueryFactory as qf
            >>> query = qf.between('member_field:some_numeric_field', 5, 10)
            >>> query.to_tuple()
            ("member_field:some_numeric_field", "between", 5, 10)

        """
        return operator.BetweenQuery(field, low, high)

    @staticmethod
    def in_last(field, interval):
        """
        In Last Query Factory

        :param field: Field name to query
        :type field: :class:`str`
        :param interval: An interval to select
        :type interval: :class:`dict`

        Usage::

            >>> from emma.query.factory import QueryFactory as qf
            >>> query = qf.in_last('member_since', {"day": 4})
            >>> query.to_tuple()
            ("member_since", "in last", {"day": 4})

        """
        return operator.InLastQuery(field, interval)

    @staticmethod
    def in_next(field, interval):
        """
        In Next Query Factory

        :param field: Field name to query
        :type field: :class:`str`
        :param interval: An interval to select
        :type interval: :class:`dict`

        Usage::

            >>> from emma.query.factory import QueryFactory as qf
            >>> query = qf.in_next('member_since', {"day": 4})
            >>> query.to_tuple()
            ("member_since", "in next", {"day": 4})

        """
        return operator.InNextQuery(field, interval)

    @staticmethod
    def datematch(field, date):
        """
        Date Match Query Factory

        :param field: Field name to query
        :type field: :class:`str`
        :param date: An date to select
        :type date: :class:`dict`

        Usage::

            >>> from emma.query.factory import QueryFactory as qf
            >>> query = qf.datematch('member_since', {"year": 2011})
            >>> query.to_tuple()
            ("member_since", "datematch", {"year": 2011})

        """
        return operator.DateMatchQuery(field, date)

    @staticmethod
    def contains(field, value):
        """
        Contains Query Factory

        :param field: Field name to query
        :type field: :class:`str`
        :param value: Value to select
        :type value: :class:`str`
        :rtype: :class:`CompositeQuery`

        Usage::

            >>> from emma.query.factory import QueryFactory as qf
            >>> query = qf.contains('member_field:some_string_field', '*foo*')
            >>> query.to_tuple()
            ("member_field:some_string_field", "contains", "*foo*")

        """
        return operator.ContainsQuery(field, value)

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

            >>> from emma.query.factory import QueryFactory as qf
            >>> query = qf.any('member_field:some_array_field', 'ten')
            >>> query.to_tuple()
            ("member_field:some_array_field", "any", "ten")

        """
        return operator.AnyQuery(field, value)

    @staticmethod
    def is_in(field, values):
        """
        Is In Query Factory

        :param field: Field name to query
        :type field: :class:`str`
        :param values: Values to test
        :type values: :class:`list`
        :rtype: :class:`CompositeQuery`

        Example Usage::

            >>> from emma.query.factory import QueryFactory as qf
            >>> query = qf.is_in('member_field:some_number_field', [3, 4, 5, 6])
            >>> query.to_tuple()
            ("member_field:some_number_field", "in", 3, 4, 5, 6)

        """
        return operator.IsInQuery(field, values)

    @staticmethod
    def zip_radius(field, radius, zip):
        """
        Zip Radius Query Factory

        :param field: Field name to query
        :type field: :class:`str`
        :param radius: The radius to select
        :type radius: :class:`int`
        :param zip: The zip code to select
        :type zip: :class:`int` or :class:`str`
        :rtype: :class:`CompositeQuery`

        Example Usage::

            >>> from emma.query.factory import QueryFactory as qf
            >>> query = qf.zip_radius('member_field:some_zipcode_field', 10, "97202")
            >>> query.to_tuple()
            ("member_field:some_zipcode_field", "zip-radius:10", "97202")

        """
        return operator.ZipRadiusQuery(field, radius, zip)
