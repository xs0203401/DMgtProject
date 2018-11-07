es=Employee.objects.exclude(pk=6)
for i in range(8,-1,-1):
  for e in es:
    e.point_tosd=1000
    e.point_recd=10000
    e.save()
  g.generate_data(n=30,num_month_ago=i)