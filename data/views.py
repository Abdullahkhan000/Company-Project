from rest_framework.views import APIView
from yaml import serialize
from rest_framework import generics
from django.shortcuts import render , get_object_or_404
from .serializer import (
    BirthSerializer,
    SocialSerializer,
    EducationSerializer,
    TotalInfoSerializer,
    CompanySerializer,
)
from .models import Birth, Social, Education, TotalInfo, Company
from rest_framework import status
from rest_framework.response import Response
from .permission import IsOwnerOrAdmin, ReadPerm
from .filters import (
    BirthFilter,
    SocialFilter,
    EducationFilter,
    TotalInfoFilterSet,
    CompanyFilterSet,
)
from rest_framework.filters import SearchFilter , OrderingFilter


# class BirthViews(APIView):
#     permission_classes = [IsOwnerOrAdmin, ReadPerm]
#
#     def get_object(self, pk):
#         try:
#             return Birth.objects.get(pk=pk)
#         except Birth.DoesNotExist:
#             return None
#
#     def get(self, request, pk=None):
#         if pk is not None:
#             obj = self.get_object(pk)
#             if not obj:
#                 return Response(
#                     {
#                         "success": False,
#                         "message": "No records found for the given id.",
#                     },
#                     status=status.HTTP_404_NOT_FOUND,
#                 )
#             serializer = BirthSerializer(obj)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#
#         else:
#             name = request.GET.get("name")
#             anon_id = request.GET.get("anon_id")
#
#         for key in request.GET.keys():
#             if key not in ["name", "anon_id"]:
#                 return Response(
#                     {"error": f"Invalid filter: {key}"},
#                     status=status.HTTP_400_BAD_REQUEST,
#                 )
#
#         queryset = Birth.objects.all()
#
#         if name:
#             queryset = queryset.filter(name=name)
#
#         if anon_id:
#             queryset = queryset.filter(anon_id=anon_id)
#
#         if not queryset.exists():
#             return Response(
#             {
#                 "success": False,
#                 "message": "No records found for the given filters.",
#                 "filters": request.GET,
#             },
#             status=status.HTTP_404_NOT_FOUND,
#         )
#
#         serializer = BirthSerializer(queryset, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#     def post(self, request, pk=None):
#         if pk is not None:
#             return Response(
#                 "error:No Post in ID data", status=status.HTTP_401_UNAUTHORIZED
#             )
#         else:
#             serializer = BirthSerializer(
#                 data=request.data, context={"request": request}
#             )
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data, status=status.HTTP_201_CREATED)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def patch(self, request, pk=None):
#         if pk is None:
#             return Response(
#                 {"error": "No Data Entry Without Entering ID"},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )
#
#         obj = self.get_object(pk)
#         if not obj:
#             return Response(
#                 {"error": "Object not found"}, status=status.HTTP_404_NOT_FOUND
#             )
#
#         serializer = BirthSerializer(
#             obj, data=request.data, partial=True, context={"request": request}
#         )
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def put(self, request, pk=None):
#         if pk is None:
#             return Response(
#                 {"error": "No Data Entry Without Entering ID"},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )
#
#         obj = self.get_object(pk)
#         if not obj:
#             return Response(
#                 {"error": "Object not found"}, status=status.HTTP_404_NOT_FOUND
#             )
#
#         serializer = BirthSerializer(
#             obj, data=request.data, context={"request": request}
#         )
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk=None):
#         if pk is not None:
#             obj = self.get_object(pk)
#             if not obj:
#                 return Response(
#                     {"error": "Operation Error Not Found"},
#                     status=status.HTTP_404_NOT_FOUND,
#                 )
#             obj.delete()
#             return Response(
#                 {"Operation Successful": "Object Deleted"},
#                 status=status.HTTP_202_ACCEPTED,
#             )
#         else:
#             return Response(
#                 {"error": "Delete Cannot Work Without Primary Key"},
#                 status=status.HTTP_401_UNAUTHORIZED,
#             )


class BirthViews(APIView):
    permission_classes = [IsOwnerOrAdmin, ReadPerm]

    def get_object(self, pk):
        try:
            return Birth.objects.get(pk=pk)
        except Birth.DoesNotExist:
            return None

    def get(self, request, pk=None):
        if pk is not None:
            obj = self.get_object(pk)
            if not obj:
                return Response(
                    {"success": False, "message": "No records found for the given id."},
                    status=status.HTTP_404_NOT_FOUND,
                )
            serializer = BirthSerializer(obj)
            return Response(serializer.data, status=status.HTTP_200_OK)

        queryset = Birth.objects.all()

        filterset = BirthFilter(request.GET, queryset=queryset)

        if not filterset.is_valid():
            return Response(filterset.errors, status=status.HTTP_400_BAD_REQUEST)

        queryset = filterset.qs

        if not queryset.exists():
            return Response(
                {
                    "success": False,
                    "message": "No records found for the given filters.",
                    "filters": request.GET,
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = BirthSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk=None):
        if pk is not None:
            return Response(
                {"error": "Cannot POST with an ID"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = BirthSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk=None):
        if pk is None:
            return Response(
                {"error": "ID required for PATCH"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        obj = self.get_object(pk)
        if not obj:
            return Response(
                {"error": "Object not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = BirthSerializer(
            obj, data=request.data, partial=True, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        if pk is None:
            return Response(
                {"error": "ID required for PUT"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        obj = self.get_object(pk)
        if not obj:
            return Response(
                {"error": "Object not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = BirthSerializer(
            obj, data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        if pk is None:
            return Response(
                {"error": "Delete requires an ID"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        obj = self.get_object(pk)
        if not obj:
            return Response(
                {"error": "Object not found"}, status=status.HTTP_404_NOT_FOUND
            )
        obj.delete()
        return Response({"message": "Object deleted"}, status=status.HTTP_202_ACCEPTED)


# Social Views Without Defining get_object function

# class SocialViews(APIView):
#     def get(self, request, pk=None):
#         if pk is not None:
#             # Path parameter filtering
#             try:
#                 obj = Social.objects.get(pk=pk)
#                 serializer = SocialSerializer(obj)
#                 return Response(serializer.data, status=status.HTTP_200_OK)
#             except Social.DoesNotExist:
#                 return Response({"error": "Data Not Found"}, status=status.HTTP_404_NOT_FOUND)
#         else:
#
#             name = request.GET.get('name')
#             obj_id = request.GET.get('id')
#
#             for key in request.GET.keys():
#                 if key not in ["name", "id"]:
#                     return Response(
#                         {"error": f"Invalid filter: {key}"},
#                         status=status.HTTP_400_BAD_REQUEST
#                     )
#
#             queryset = Social.objects.all()
#
#             if name:
#                 queryset = queryset.filter(name__name=name)
#
#             if obj_id:
#                 queryset = queryset.filter(pk=obj_id)
#
#             if not queryset.exists():
#                 return Response({"error": "Not Found"}, status=status.HTTP_404_NOT_FOUND)
#
#             serializer = SocialSerializer(queryset, many=True)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#
#     def post(self, request, pk=None):
#         if pk is not None:
#             return Response(
#                 {"error": "POST cannot be used with a primary key"},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )
#
#         serializer = SocialSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(
#                 {"message": "Data created successfully"},
#                 status=status.HTTP_201_CREATED,
#             )
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def patch(self, request, pk=None):
#         if pk is None:
#             return Response(
#                 {"error": "PATCH requires a primary key"},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )
#
#         try:
#             obj = Social.objects.get(pk=pk)
#         except Social.DoesNotExist:
#             return Response({"error": "Object not found"}, status=status.HTTP_404_NOT_FOUND)
#
#         serializer = SocialSerializer(obj, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def put(self, request, pk=None):
#         if pk is None:
#             return Response(
#                 {"error": "PUT requires a primary key"},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )
#
#         try:
#             obj = Social.objects.get(pk=pk)
#         except Social.DoesNotExist:
#             return Response({"error": "Object not found"}, status=status.HTTP_404_NOT_FOUND)
#
#         serializer = SocialSerializer(obj, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self,request,pk=None):
#         if pk is not None:
#             try:
#                 obj = Social.objects.get(pk=pk)
#                 obj.delete()
#                 return Response({"Operation Successful":"Object Deleted"},status=status.HTTP_202_ACCEPTED)
#             except Social.DoesNotExist:
#                 return Response({"error":"Operation Error Not Found"},status=status.HTTP_404_NOT_FOUND)
#         else:
#             return Response({"error":"Delete Cannot Work Without Primary Key"},status=status.HTTP_401_UNAUTHORIZED)


# class SocialViews(APIView):
#     def get_object(self, pk):
#         try:
#             return Social.objects.get(pk=pk)
#         except Social.DoesNotExist:
#             return None
#
#     # ---------------- GET ---------------- #
#     def get(self, request, pk=None):
#         if pk is not None:
#             obj = self.get_object(pk)
#             if not obj:
#                 return Response(
#                     {
#                         "success": False,
#                         "message": "No records found for the given id.",
#                     },
#                     status=status.HTTP_404_NOT_FOUND,
#                 )
#
#             serializer = SocialSerializer(obj)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#
#         # Query Parameter Filtering
#         name = request.GET.get("name")
#         obj_id = request.GET.get("id")
#
#         for key in request.GET.keys():
#             if key not in ["name", "id"]:
#                 return Response(
#                     {"error": f"Invalid filter: {key}"},
#                     status=status.HTTP_400_BAD_REQUEST,
#                 )
#
#         queryset = Social.objects.all()
#
#         if name:
#             queryset = queryset.filter(name__name=name)
#         if obj_id:
#             queryset = queryset.filter(pk=obj_id)
#
#         if not queryset.exists():
#             return Response(
#                 {
#                     "success": False,
#                     "message": "No records found for the given filters.",
#                     "filters": request.GET,
#                 },
#                 status=status.HTTP_404_NOT_FOUND,
#             )
#
#         serializer = SocialSerializer(queryset, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#     # ---------------- POST ---------------- #
#     def post(self, request, pk=None):
#         if pk is not None:
#             return Response(
#                 {"error": "POST cannot be used with a primary key"},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )
#
#         serializer = SocialSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(
#                 {"message": "Data created successfully"},
#                 status=status.HTTP_201_CREATED,
#             )
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     # ---------------- PATCH ---------------- #
#     def patch(self, request, pk=None):
#         if pk is None:
#             return Response(
#                 {"error": "PATCH requires a primary key"},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )
#
#         obj = self.get_object(pk)
#         if not obj:
#             return Response(
#                 {"error": "Object not found"}, status=status.HTTP_404_NOT_FOUND
#             )
#
#         serializer = SocialSerializer(obj, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     # ---------------- PUT ---------------- #
#     def put(self, request, pk=None):
#         if pk is None:
#             return Response(
#                 {"error": "PUT requires a primary key"},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )
#
#         obj = self.get_object(pk)
#         if not obj:
#             return Response(
#                 {"error": "Object not found"}, status=status.HTTP_404_NOT_FOUND
#             )
#
#         serializer = SocialSerializer(obj, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     # ---------------- DELETE ---------------- #
#     def delete(self, request, pk=None):
#         if pk is not None:
#             obj = self.get_object(pk)
#             if not obj:
#                 return Response(
#                     {"error": "Operation Error Not Found"},
#                     status=status.HTTP_404_NOT_FOUND,
#                 )
#
#             obj.delete()
#             return Response(
#                 {"Operation Successful": "Object Deleted"},mai
#                 status=status.HTTP_202_ACCEPTED,
#             )
#         else:
#             return Response(
#                 {"error": "Delete Cannot Work Without Primary Key"},
#                 status=status.HTTP_401_UNAUTHORIZED,
#             )


class SocialViews(APIView):
    def get_object(self, pk):
        try:
            return Social.objects.get(pk=pk)
        except Social.DoesNotExist:
            return None

    # ---------------- GET ---------------- #
    def get(self, request, pk=None):
        if pk is not None:
            obj = self.get_object(pk)
            if not obj:
                return Response(
                    {
                        "success": False,
                        "message": "No records found for the given id.",
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )

            serializer = SocialSerializer(obj)
            return Response(serializer.data, status=status.HTTP_200_OK)

        queryset = Social.objects.all()

        filterset = SocialFilter(request.GET, queryset=queryset)

        if not filterset.is_valid():
            return Response(filterset.errors, status=status.HTTP_400_BAD_REQUEST)

        queryset = filterset.qs

        if not queryset.exists():
            return Response(
                {
                    "success": False,
                    "message": "No records found for the given filters.",
                    "filters": request.GET,
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = SocialSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # ---------------- POST ---------------- #
    def post(self, request, pk=None):
        if pk is not None:
            return Response(
                {"error": "POST cannot be used with a primary key"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = SocialSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Data created successfully"},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # ---------------- PATCH ---------------- #
    def patch(self, request, pk=None):
        if pk is None:
            return Response(
                {"error": "PATCH requires a primary key"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        obj = self.get_object(pk)
        if not obj:
            return Response(
                {"error": "Object not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = SocialSerializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # ---------------- PUT ---------------- #
    def put(self, request, pk=None):
        if pk is None:
            return Response(
                {"error": "PUT requires a primary key"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        obj = self.get_object(pk)
        if not obj:
            return Response(
                {"error": "Object not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = SocialSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # ---------------- DELETE ---------------- #
    def delete(self, request, pk=None):
        if pk is not None:
            obj = self.get_object(pk)
            if not obj:
                return Response(
                    {"error": "Operation Error Not Found"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            obj.delete()
            return Response(
                {"Operation Successful": "Object Deleted"},
                status=status.HTTP_202_ACCEPTED,
            )
        else:
            return Response(
                {"error": "Delete Cannot Work Without Primary Key"},
                status=status.HTTP_401_UNAUTHORIZED,
            )


class EducationViews(APIView):
    def get_object(self, pk):
        try:
            return Education.objects.get(pk=pk)
        except Education.DoesNotExist:
            return None

    def get(self, request, pk=None):
        if pk is not None:
            obj = self.get_object(pk)
            if not obj:
                return Response(
                    {
                        "success": False,
                        "message": "No records found for the given id.",
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )

            serializer = EducationSerializer(obj)
            return Response(serializer.data, status=status.HTTP_200_OK)

        queryset = Education.objects.all()
        filterset = EducationFilter(request.GET, queryset=queryset)

        if not filterset.is_valid():
            return Response(filterset.errors, status=status.HTTP_400_BAD_REQUEST)

        queryset = filterset.qs

        search = SearchFilter()
        self.search_fields = ["school", "class_number"]
        queryset = search.filter_queryset(request, queryset, self)

        if not queryset.exists():
            return Response(
                {
                    "success": False,
                    "message": "No records found for the given filters.",
                    "filters": request.GET,
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = EducationSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk=None):
        if pk is not None:
            return Response(
                {"error": "POST cannot be used with a primary key"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = EducationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Data created successfully"},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk=None):
        if pk is None:
            return Response(
                {"error": "PATCH requires a primary key"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        obj = self.get_object(pk)
        if not obj:
            return Response(
                {"error": "Object not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = EducationSerializer(obj, partial=True, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        if pk is None:
            return Response(
                {"error": "PUT requires a primary key"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        obj = self.get_object(pk)
        if not obj:
            return Response(
                {"error": "Object not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = EducationSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        if pk is not None:
            obj = self.get_object(pk)
            if not obj:
                return Response(
                    {"error": "Operation Error Not Found"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            obj.delete()
            return Response(
                {"Operation Successful": "Object Deleted"},
                status=status.HTTP_202_ACCEPTED,
            )
        else:
            return Response(
                {"error": "Delete Cannot Work Without Primary Key"},
                status=status.HTTP_401_UNAUTHORIZED,
            )


# class TotalInfoViews(APIView):
#     def get_object(self,pk):
#         try:
#             return TotalInfo.objects.get(pk=pk)
#         except TotalInfo.DoesNotExist:
#             return None
#
#     def get(self,request,pk=None):
#         if pk is not None:
#             obj = self.get_object(pk)
#             if not obj:
#                 return Response(
#                     {
#                         "success": False,
#                         "message": "No records found for the given id.",
#                     },
#                     status=status.HTTP_404_NOT_FOUND,
#                 )
#         queryset = TotalInfo.objects.all()
#         filterset = TotalInfoFilterSet(request.GET,queryset=queryset)
#
#         queryset = filterset.qs
#         if not queryset.exists():
#             return Response(
#                 {
#                     "success": False,
#                     "message": "No records found for the given filters.",
#                     "filters": request.GET,
#                 },
#                 status=status.HTTP_404_NOT_FOUND,
#             )
#
#         serializer = TotalInfoSerializer(queryset, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)


class TotalInfoViews(APIView):
    def get(self, request, pk=None):
        if pk:
            try:
                obj = TotalInfo.objects.get(pk=pk)
            except TotalInfo.DoesNotExist:
                return Response(
                    {"success": False, "message": "No record found."},
                    status=status.HTTP_404_NOT_FOUND,
                )
            return Response(TotalInfoSerializer(obj).data, status=status.HTTP_200_OK)

        queryset = TotalInfo.objects.all()
        filterset = TotalInfoFilterSet(request.GET, queryset=queryset)

        if not filterset.is_valid():
            return Response(filterset.errors, status=status.HTTP_400_BAD_REQUEST)

        queryset = filterset.qs

        search_filter = SearchFilter()
        self.search_fields = ["birth__name", "education__school", "social__email"]
        queryset = search_filter.filter_queryset(request, queryset, self)

        if not queryset.exists():
            return Response(
                {"success": False, "message": "No results found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(
            TotalInfoSerializer(queryset, many=True).data, status=status.HTTP_200_OK
        )

class CompanyViews(APIView):
    search_fields = ["name", "address", "status", "website", "join"]
    ordering_fields = ["name", "total_workers", "status", "join"]

    def get_object(self, pk):
        try:
            return Company.objects.get(pk=pk)
        except Company.DoesNotExist:
            return None

    def get(self, request, pk=None):
        if pk:
            obj = self.get_object(pk)
            if not obj:
                return Response(
                    {"success": False, "message": "No record found."},
                    status=status.HTTP_404_NOT_FOUND,
                )
            return Response(CompanySerializer(obj).data, status=status.HTTP_200_OK)

        queryset = Company.objects.all()
        filterset = CompanyFilterSet(request.GET, queryset=queryset)

        if not filterset.is_valid():
            return Response(filterset.errors, status=status.HTTP_400_BAD_REQUEST)

        queryset = filterset.qs

        search_filter = SearchFilter()
        queryset = search_filter.filter_queryset(request, queryset, self)

        order_filter = OrderingFilter()
        queryset = order_filter.filter_queryset(request, queryset, self)

        if not queryset.exists():
            return Response(
                {"success": False, "message": "No results found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(
            CompanySerializer(queryset, many=True).data, status=status.HTTP_200_OK
        )

    def post(self, request, pk=None):
        if pk is not None:
            return Response({"error": "POSt cannot use in Primary key"})

        serializer = CompanySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Data created successfully"},
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk=None):
        if pk is None:
            return Response(
                {"error": "PATCH requires a primary key"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        obj = self.get_object(pk)
        if not obj:
            return Response(
                {"error": "Data Not Found"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = CompanySerializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Data created successfully"},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        if pk is None:
            return Response(
                {"error": "PUT requires a primary key"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        obj = self.get_object(pk)
        if not obj:
            return Response(
                {"error": "Data Not Found"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = CompanySerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Data created successfully"},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        if pk is not None:
            obj = self.get_object(pk)
            if not obj:
                return Response(
                    {"error": "Operation Error Not Found"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            obj.delete()
            return Response(
                {"Operation Successful": "Object Deleted"},
                status=status.HTTP_202_ACCEPTED,
            )
        else:
            return Response(
                {"error": "Delete Cannot Work Without Primary Key"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

def company_template_view(request, pk=None):
    if pk is not None:
        company = get_object_or_404(Company, pk=pk)
        return render(request, 'company/company.html', {'company': company})
    else:
        companies = Company.objects.all()
        return render(request, 'company/company.html', {"companies": companies})