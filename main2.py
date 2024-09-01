
import pytesseract
from PIL import Image
import subprocess
import os

# Define paths
old_images = "old_images.txt"
images_folder = "images/"
budgetsFile = "budget.txt"

transactions_file = "transactions.txt"
# Get all image names
output = subprocess.check_output(["ls", images_folder], text=True)

separators = [
        "minutesago", 
        "minuteago", 
        "hourago", 
        "hoursago",
        "daysago",
        "weekago", 
        "weeksago",
        "minutes ago", 
        "minute ago", 
        "hour ago", 
        "hours ago",
        "Yesterday",
        "days ago",
        "week ago", 
        "weeks ago",
        "9a/mago"]
# Split output into a list of image names
images = output.strip().split("\n")

f=  open(old_images, "r") 
old_imagesT= f.read()
f.close()

def getBudgets():
    #read actual budget 
    f = open(budgetsFile, "r+")
    budgets = f.readlines()
    budgets = [[budget.split(":")[0], int(budget.split(": ")[1])] for budget in budgets]
    f.close()
    return budgets

def setBudgets(budgets):
    #set updated budget 
    f = open(budgetsFile, "w")
    for budget in budgets:
        budget[1] = str(budget[1])
    budgets = [": ".join(budget) for budget in budgets]
    fb = ("\n".join(budgets))
    f.write(fb)
    f.close()

def extract_team_and_amount(transactions):
    result = []

    for transaction in transactions:
        # Strip leading/trailing whitespace
        transaction = transaction.strip()

        sign = 1
        # Split on "has sold" or "bought" to isolate team name and amount
        if "has sold" in transaction:
            team, amount_part = transaction.split("has sold")
        elif "bought" in transaction:
            team, amount_part = transaction.split("bought")
            sign = -1

        # Extract the numeric value before the €
        amount = sign * int(amount_part.split("€")[0].split()[-1].replace('.', '').replace(',', ''))

        # Append the team name (trimmed) and the amount to the result list
        result.append([team.strip(), amount])

    return result

def checkRepeated(transaction, transactions):
    if transaction in transactions:
        print("REPETIDA!!!!!"*100)
        exit(0)

def appendTransactions(transactions):
    f = open(transactions_file, "a+")
    f.write("\n".join(transactions))
    f.close()

def getTransactions():
    f = open(transactions_file, "r+")
    transactions = f.read()
    f.close()
    return transactions
    


problemas_encontrados = 0
# Process each image
for image_name in images:
    if image_name in old_imagesT:
        continue

    old_transactions = getTransactions()
    # Full path to the image
    image_path = os.path.join(images_folder, image_name)
    
    # Open the image file
    img = Image.open(image_path)
    
    # Perform OCR on the image
    text = pytesseract.image_to_string(img)
    
    # Print the extracted text
    print(f"Imagen: {image_name}:")
    lines = text.split("\n")
    
    not_null_lines = []
    for line in lines:
        if len(line):
            not_null_lines.append(line)

    SEPARATOR = "SEPARATOR||SEPARATOR"
    for i in range(len(not_null_lines)):
        for separator in separators:
            if separator in not_null_lines[i]:
                not_null_lines[i] = SEPARATOR
                break

    list1 = ((" ".join(not_null_lines)).split(SEPARATOR))
    transactions =[]
    for it in list1:
        if "bought" in it or "has sold" in it:
            transactions.append(it)

            checkRepeated(it, old_transactions)
    
    
    appendTransactions(transactions)
    ll = extract_team_and_amount(transactions)

    budgets = getBudgets()
    contador = [0] * len(ll)
    for budget in budgets:
        for i in range(len(ll)):
            if budget[0] == ll[i][0]:
                budget[1]+= ll[i][1]

                contador[i] = 1
    
    print(contador)
    for i in range(len(contador)):
        if contador[i] == 0:
            print("Problemas en:")
            print(ll[i])
    
            correct_name = input(f"Introduce nombre correcto\n>").strip()
            for budget in budgets:
                if budget[0] == correct_name:
                    budget[1]+= ll[i][1]
                    print(ll[i][1], "sumados a", correct_name)

    setBudgets(budgets)
    print("=" * 40)

# Save the list of processed images
with open(old_images, "w") as f:
    f.write(output)


budgets = getBudgets()



for budget in budgets:
    print(budget)
    
manual = True
while(manual):
    name_quantity = input("Introduce nombre, cantidad | o end para acabar\n>").split(",")
    if name_quantity[0] == "end":
        manual = False
    else:
        name_quantity[1] = int(name_quantity[1])
        for budget in budgets:
            if budget[0] == name_quantity[0]:
                budget[1]+= name_quantity[1]
                print(name_quantity[1], "sumados a", correct_name)

for budget in budgets:
    print(budget)

setBudgets(budgets)
