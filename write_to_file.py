import csv


def write(request):
    with open('output/tasks_kaiten.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='|')
        writer.writerow(["Username", "Task", "Date"])
        for res in request:
            writer.writerow([res[0], res[1], res[2]])
