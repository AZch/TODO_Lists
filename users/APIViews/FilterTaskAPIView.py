import re

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from Converts import DBtoObject
from WordConst import Filter, Roles, Status
from users.models import Todotbl

"""
validate count word status
"""
validate_word_status = lambda filter_data, separator: filter_data.split(separator)[1] \
                                                      if len(filter_data.split(separator)) == 2 \
                                                      else ""

"""
validate status user
"""
validate_status = lambda str: str if str == Status.new else \
                              str if str == Status.start else \
                              str if str == Status.work else \
                              str if str == Status.pause else \
                              str if str == Status.end else ""

"""
validate priority user
"""
validate_priority = lambda num_str: int(re.findall('\d+', num_str)[0]) \
                                    if len(re.findall('\d+', num_str)) == 1 \
                                    else 0

# class to store filter element
class FilterData():
    def __init__(self, columnName='', val=''):
        self.columnName = columnName
        self.val = val
        self.isMore = False
        self.isLess = False
        self.isEqual = False


class FilterTaskAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """
        search filter in TODOs
        :param request: send in body data like {"column": "priority>=2,prioritydesc"} to "and" search (priorityasc,
        priority<5,statusasc,statusdesc,status=new,...)
        :return:
        """
        TODOs = Todotbl.objects.all() if request.user.role == Roles.admin else Todotbl.objects.filter(user=request.user)
        for filterData in re.split(Filter.separator, request.data[Filter.column]):
            filterDataMake = FilterData()
            # set column to search
            if Filter.column_priority in filterData:
                filterDataMake.columnName = Filter.column_priority
            elif Filter.column_status in filterData:
                filterDataMake.columnName = Filter.column_status

            # what search (order by or filtering)
            if Filter.asc in filterData:  # order by asc
                filterDataMake.val = Filter.asc
                TODOs = Todotbl.objects.filter(id__in=TODOs).order_by(filterDataMake.columnName).distinct()
            elif Filter.desc in filterData:  # order by desc
                filterDataMake.val = Filter.desc
                TODOs = Todotbl.objects.filter(id__in=TODOs).order_by(filterDataMake.columnName).reverse().distinct()
            else:
                if Filter.more in filterData:  # if more
                    filterDataMake.isMore = True
                elif Filter.less in filterData:  # if less
                    filterDataMake.isLess = True

                if Filter.equal in filterData:  # if equal
                    filterDataMake.isEqual = True
                    if filterDataMake.isMore:  # if more equal
                        if Filter.column_priority == filterDataMake.columnName:  # if more equal in column priority
                            TODOs = Todotbl.objects.filter(id__in=TODOs,
                                                           priority__gte=validate_priority(filterData)).distinct()
                        elif Filter.column_status == filterDataMake.columnName:  # if more equal in column status
                            TODOs = Todotbl.objects.filter(id__in=TODOs,
                                                           status__gte=validate_status(
                                                               validate_word_status(filterData, '>='))) \
                                .distinct()
                    elif filterDataMake.isLess:  # if less equal
                        if Filter.column_priority == filterDataMake.columnName:   # if less equal in column priority
                            TODOs = Todotbl.objects.filter(id__in=TODOs,
                                                           priority__lte=validate_priority(filterData)).distinct()
                        elif Filter.column_status == filterDataMake.columnName:  # if less equal in column status
                            TODOs = Todotbl.objects.filter(id__in=TODOs,
                                                           status__lte=validate_status(
                                                               validate_word_status(filterData, '<='))).distinct()
                    else:  # if equal
                        if Filter.column_priority == filterDataMake.columnName:  # if equal in column priority
                            TODOs = Todotbl.objects.filter(id__in=TODOs,
                                                           priority=validate_priority(filterData)).distinct()
                        elif Filter.column_status == filterDataMake.columnName:  # if equal in column status
                            TODOs = Todotbl.objects.filter(id__in=TODOs,
                                                           status=validate_status(
                                                               validate_word_status(filterData, '='))).distinct()

                else:  # if not equal, only more or less
                    if filterDataMake.isMore:  # if more
                        if Filter.column_priority == filterDataMake.columnName:  # if more in column priority
                            TODOs = Todotbl.objects.filter(id__in=TODOs,
                                                           priority__gt=validate_priority(filterData)).distinct()
                        elif Filter.column_status == filterDataMake.columnName:  # if more in column status
                            TODOs = Todotbl.objects.filter(id__in=TODOs,
                                                           status__gt=validate_status(
                                                               validate_word_status(filterData, '>'))).distinct()
                    else:  # if less
                        if Filter.column_priority == filterDataMake.columnName:  # if less in column priority
                            TODOs = Todotbl.objects.filter(id__in=TODOs,
                                                           priority__lt=validate_priority(filterData)).distinct()
                        elif Filter.column_status == filterDataMake.columnName:  # if less in column status
                            TODOs = Todotbl.objects.filter(id__in=TODOs,
                                                           status__lt=validate_status(
                                                               validate_word_status(filterData, '<'))).distinct()
        return Response(DBtoObject.dictTODOs(TODOs), status=status.HTTP_200_OK)
