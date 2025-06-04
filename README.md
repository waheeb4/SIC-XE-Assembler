SIC/XE Two-Pass Assembler
This project is a Python-based implementation of a two-pass assembler for the SIC/XE (Simplified Instructional Computer / Extra Equipment) architecture. It parses, processes, and assembles assembly language source code into object code, following the standard SIC/XE instruction set and addressing modes.

🚀 Features
✅ Supports Formats 1, 2, 3, and 4 instructions.

🧠 Implements pass 1 to:

Build the symbol table (SYMTAB)
Calculate location counters (LOCCTR)
Generate an intermediate file with addresses

🔄 Implements pass 2 to:

Generate object code using addressing modes: immediate (#), indirect (@), simple, and indexed
Handle PC-relative and Base-relative addressing

🧾 Output:

HTME
