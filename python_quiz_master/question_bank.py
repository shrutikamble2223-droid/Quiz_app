"""Built-in quiz content for Python Quiz Master."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Question:
    category: str
    difficulty: str
    prompt: str
    options: tuple[str, str, str, str]
    answer: str
    explanation: str


_RAW = [
    # Python Programming
    ("Python Programming", "Easy", "Which keyword defines a function?", ("func", "def", "function", "lambda"), "def", "The def keyword begins a named function definition."),
    ("Python Programming", "Easy", "Which type is mutable?", ("tuple", "str", "list", "frozenset"), "list", "Lists can be changed after they are created."),
    ("Python Programming", "Easy", "What does len([3, 5, 7]) return?", ("2", "3", "7", "15"), "3", "len returns the number of items in the list."),
    ("Python Programming", "Easy", "Which symbol starts a comment?", ("//", "#", "--", "/*"), "#", "Python uses # for a single-line comment."),
    ("Python Programming", "Easy", "What is the result of 2 ** 3?", ("6", "8", "9", "5"), "8", "The ** operator raises the left operand to a power."),
    ("Python Programming", "Easy", "Which value represents absence of a value?", ("void", "None", "null", "empty"), "None", "Python uses the singleton None for an absent value."),
    ("Python Programming", "Easy", "How do you add item x to the end of list a?", ("a.push(x)", "a.add(x)", "a.append(x)", "a.insertEnd(x)"), "a.append(x)", "list.append adds one item at the end."),
    ("Python Programming", "Medium", "What does dict.get('x', 0) do when x is absent?", ("Raises KeyError", "Returns 0", "Adds x", "Returns None always"), "Returns 0", "get returns its supplied default when the key is missing."),
    ("Python Programming", "Medium", "Which expression creates a shallow list copy?", ("a.copy()", "copy(a, deep=True)", "a.clone()", "a = a"), "a.copy()", "The list copy method creates a shallow copy."),
    ("Python Programming", "Medium", "What does enumerate(items) yield?", ("Values only", "Index-value pairs", "Keys only", "A sorted list"), "Index-value pairs", "enumerate yields pairs containing a counter and each item."),
    ("Python Programming", "Medium", "Which block runs whether or not an exception occurs?", ("except", "else", "finally", "raise"), "finally", "A finally block runs during both successful and exceptional exits."),
    ("Python Programming", "Medium", "What is a lambda in Python?", ("Anonymous function", "Package manager", "Loop type", "Class decorator"), "Anonymous function", "lambda creates a small anonymous function expression."),
    ("Python Programming", "Hard", "What does a generator function yield?", ("A lazy iterator", "A thread", "A tuple only", "A module"), "A lazy iterator", "yield suspends a function and produces values on demand."),
    ("Python Programming", "Hard", "What is the main purpose of __init__?", ("Initialize a new instance", "Delete an instance", "Import a module", "Compare objects"), "Initialize a new instance", "__init__ initializes state after an instance is created."),
    # General Knowledge
    ("General Knowledge", "Easy", "What is the capital of Japan?", ("Kyoto", "Tokyo", "Osaka", "Nagoya"), "Tokyo", "Tokyo is Japan's capital and largest metropolitan center."),
    ("General Knowledge", "Easy", "How many days are in a leap year?", ("364", "365", "366", "367"), "366", "A leap year adds February 29, making 366 days."),
    ("General Knowledge", "Easy", "Which ocean is the largest?", ("Atlantic", "Indian", "Arctic", "Pacific"), "Pacific", "The Pacific is the largest and deepest ocean."),
    ("General Knowledge", "Easy", "Which planet is known as the Red Planet?", ("Venus", "Mars", "Jupiter", "Mercury"), "Mars", "Iron-rich dust gives Mars its reddish appearance."),
    ("General Knowledge", "Easy", "What is the currency of the United Kingdom?", ("Euro", "Pound sterling", "Dollar", "Franc"), "Pound sterling", "The pound sterling is the UK's currency."),
    ("General Knowledge", "Medium", "Who wrote the play Hamlet?", ("Charles Dickens", "William Shakespeare", "Jane Austen", "George Orwell"), "William Shakespeare", "Hamlet is a tragedy by William Shakespeare."),
    ("General Knowledge", "Medium", "Which country is home to the Great Pyramid of Giza?", ("Mexico", "Egypt", "Greece", "Jordan"), "Egypt", "The Giza pyramid complex is in Egypt, near Cairo."),
    ("General Knowledge", "Medium", "What is the smallest continent by land area?", ("Europe", "Australia", "Antarctica", "South America"), "Australia", "Australia is the smallest of the commonly defined continents."),
    ("General Knowledge", "Hard", "Which strait separates Europe and Africa at their closest point?", ("Bering Strait", "Strait of Gibraltar", "Bosporus", "Dover Strait"), "Strait of Gibraltar", "The Strait of Gibraltar separates Spain and Morocco."),
    ("General Knowledge", "Hard", "In which year did the first Moon landing occur?", ("1965", "1969", "1972", "1959"), "1969", "Apollo 11 landed on the Moon in July 1969."),
    # Mathematics
    ("Mathematics", "Easy", "What is 12 × 8?", ("88", "96", "108", "92"), "96", "12 multiplied by 8 equals 96."),
    ("Mathematics", "Easy", "What is the square root of 81?", ("7", "8", "9", "10"), "9", "9 × 9 equals 81."),
    ("Mathematics", "Easy", "What is 15% of 200?", ("20", "25", "30", "35"), "30", "0.15 × 200 equals 30."),
    ("Mathematics", "Easy", "How many degrees are in a right angle?", ("45", "90", "180", "360"), "90", "A right angle measures 90 degrees."),
    ("Mathematics", "Medium", "Solve: 3x + 5 = 20", ("3", "5", "6", "8"), "5", "Subtract 5 and divide by 3 to get x = 5."),
    ("Mathematics", "Medium", "What is the area of a 7 by 4 rectangle?", ("11", "22", "28", "49"), "28", "Rectangle area is length times width: 7 × 4."),
    ("Mathematics", "Medium", "What is the median of 2, 5, 8, 11, 14?", ("5", "8", "9", "11"), "8", "The median is the middle value in the ordered list."),
    ("Mathematics", "Hard", "What is the derivative of x²?", ("x", "2x", "x³", "2"), "2x", "The power rule gives d(x²)/dx = 2x."),
    ("Mathematics", "Hard", "What is the probability of rolling an even number on a fair six-sided die?", ("1/6", "1/3", "1/2", "2/3"), "1/2", "Three of the six equally likely outcomes are even."),
    # Science
    ("Science", "Easy", "What gas do plants absorb during photosynthesis?", ("Oxygen", "Carbon dioxide", "Nitrogen", "Hydrogen"), "Carbon dioxide", "Plants use carbon dioxide and water to make sugars."),
    ("Science", "Easy", "What is the chemical symbol for water?", ("CO2", "O2", "H2O", "NaCl"), "H2O", "A water molecule contains two hydrogen atoms and one oxygen atom."),
    ("Science", "Easy", "Which force pulls objects toward Earth?", ("Friction", "Magnetism", "Gravity", "Buoyancy"), "Gravity", "Earth's gravity attracts objects toward its center."),
    ("Science", "Easy", "Which organ pumps blood through the human body?", ("Lungs", "Brain", "Heart", "Liver"), "Heart", "The heart circulates blood through the body."),
    ("Science", "Medium", "What is the center of an atom called?", ("Electron cloud", "Nucleus", "Molecule", "Orbit"), "Nucleus", "The nucleus contains protons and neutrons."),
    ("Science", "Medium", "At sea level, water boils at what temperature in Celsius?", ("0°C", "50°C", "100°C", "212°C"), "100°C", "At standard atmospheric pressure, water boils at 100°C."),
    ("Science", "Medium", "Which blood cells primarily carry oxygen?", ("Platelets", "Red blood cells", "White blood cells", "Stem cells"), "Red blood cells", "Hemoglobin in red blood cells binds and transports oxygen."),
    ("Science", "Hard", "Which particle has a negative electric charge?", ("Proton", "Neutron", "Electron", "Photon"), "Electron", "Electrons carry negative electric charge."),
    ("Science", "Hard", "What is the SI unit of electrical resistance?", ("Volt", "Ampere", "Ohm", "Watt"), "Ohm", "Electrical resistance is measured in ohms."),
    # Computer Fundamentals
    ("Computer Fundamentals", "Easy", "What does CPU stand for?", ("Central Processing Unit", "Computer Personal Unit", "Core Program Utility", "Central Power User"), "Central Processing Unit", "The CPU executes instructions and coordinates computer operations."),
    ("Computer Fundamentals", "Easy", "Which device is commonly used to point and click?", ("Monitor", "Mouse", "Speaker", "Printer"), "Mouse", "A mouse is a pointing input device."),
    ("Computer Fundamentals", "Easy", "Which is an example of an operating system?", ("Python", "Linux", "HTML", "SQLite"), "Linux", "Linux is an operating system."),
    ("Computer Fundamentals", "Easy", "What does RAM primarily provide?", ("Long-term archiving", "Temporary working memory", "Printed output", "Network routing"), "Temporary working memory", "RAM stores data and instructions in active use."),
    ("Computer Fundamentals", "Medium", "How many bits are in a byte?", ("4", "8", "16", "32"), "8", "A byte consists of eight bits."),
    ("Computer Fundamentals", "Medium", "Which protocol is commonly used to transfer web pages securely?", ("FTP", "HTTPS", "SMTP", "Telnet"), "HTTPS", "HTTPS encrypts HTTP traffic using TLS."),
    ("Computer Fundamentals", "Medium", "What is a file extension used for?", ("Identify a file's format", "Increase memory", "Encrypt a disk", "Connect a keyboard"), "Identify a file's format", "Extensions commonly indicate the file type or associated application."),
    ("Computer Fundamentals", "Hard", "Which number system uses base 2?", ("Decimal", "Hexadecimal", "Binary", "Octal"), "Binary", "Binary represents values using only 0 and 1."),
    ("Computer Fundamentals", "Hard", "What is the main role of DNS?", ("Translate domain names to IP addresses", "Compress files", "Manage printers", "Encrypt passwords"), "Translate domain names to IP addresses", "DNS resolves human-readable domain names to network addresses."),
]

QUESTIONS = tuple(Question(*row) for row in _RAW)
CATEGORIES = tuple(dict.fromkeys(q.category for q in QUESTIONS))
DIFFICULTIES = ("Easy", "Medium", "Hard")
