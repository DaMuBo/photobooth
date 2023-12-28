import cups

conn = cups.Connection()
printers = conn.getPrinters()

for printer in printers:
    print(printer)
