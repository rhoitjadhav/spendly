"""Quick Mistral categorization test — run before uploading a full PDF."""
import asyncio
import json
import os
import re
import sys

# Load .env manually
env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
if os.path.exists(env_path):
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())

from mistralai.client import Mistral
from app.services.categorizer import CATEGORIES, _SYSTEM

SAMPLE = [
    ("Payment to Swiggy", "Food order"),
    ("UPI payment to IRCTC", None),
    ("Paid to Amazon", "Birthday gift"),
    ("Transfer to Reliance Jio", "Monthly recharge"),
    ("Payment to ABC Pharmacy", None),
    # Navi-style: note carries the real meaning
    ("Paid to NZM BROADBAND", "Internet Recharge NZM"),
    ("Paid to PETROL PUMP", "Petrol 3720 ml"),
    ("Paid to CROMA", "Samsung Washing Machine 7 KG AI"),
    ("Paid to Babu", "Paani Puri"),
]

[1, "Food & Dining"], [2, "Transport"], [3, "Shopping"], [4, "Recharge"], [5, "Health"], [6, "Recharge"]

SA = ['1. Note: Dinner | Description: Paid to HOTEL ROYAL SHETKARI', '2. Note: Activa 6G Servicing | Description: Paid to APURVA AUTO AND AUTOMOBILES', '3. Note: Rickshaw to Navale Bridge | Description: Paid to ROHINI NITIN MANHERE', '4. Note: French Fryes | Description: Paid to BARATE BROTHERS', '5. Note: Lunch with Priyanka Katkar | Description: Paid to SHREE KRUSHNA PURE VEG', '6. Description: Paid to Google', '7. Note: Jio Prepaid Recharge | Description: Paid to Jio Prepaid Recharges', '8. Note: Medicines | Description: Paid to MATOSHREE MEDICAL', '9. Description: Paid to SUKUMAR MOHAN KSHIRSAGAR', '10. Note: Auto to Pune home | Description: Paid to DIPAK DATTU DINDE', '11. Note: Dal Khichadi | Description: Paid to KESHRI CHAMUNDA MAHIM HALVA', '12. Note: Sugarcane Juice | Description: Paid to SALVE CHANDRAKANT BHIVA', '13. Note: Dinner | Description: Paid to TeAmo Hospitality', '14. Note: PaymentToUBERINDIASYSTEMSPRIVATELIMITED | Description: Paid to UBER INDIA SYSTEMS PRIVATE', '15. Note: curtain for mummy | Description: Paid to AVENUE SUPERMARTS LTD', '16. Note: Pani Puri 2 | Description: Paid to SURESH KUMAR GAYRI', '17. Note: Rapido to Dmart Satara Road | Description: Paid to JAGTAP SARIKA VIJAY', '18. Note: Pay to BharatPe Merchant | Description: Paid to Aditya Satish Rokade', '19. Note: Jeera Soda | Description: Paid to AAIJI SUPER MARKET', '20. Note: zepto parcel | Description: Paid to zepto', '21. Note: Auto to Dwarika Dham | Description: Paid to SANKPAL SANTOSH KONDIRAM', '22. Note: Pay to BharatPe Merchant | Description: Paid to KEDAR PRASHANT BHAGWANRAO', '23. Note: Diet Coke | Description: Paid to DOMINOS PIZZA', '24. Note: Idli Sandwich | Description: Paid to SOUTH BOMBAY Wakad', '25. Note: Water Bottle | Description: Paid to UPSOUTH', '26. Note: Parking | Description: Paid to ALYSSUM DEVELOPERS PRIVATE', '27. Note: Petrol 2 ltr | Description: Paid to ATISH SANAS vyankateshwara', '28. Description: Bill payment of Maharashtra State Electricity', '29. Note: Uthappa | Description: Paid to PRATIBHA ENTERPRISES', '30. Note: Reshami Soya chaap | Description: Paid to RAVINDRA SHANKAR BISHUKARMA', '31. Description: Bill payment of Maharashtra State Electricity', '32. Note: Mix veg chapati 2 rice 1 vati | Description: Paid to Jaydev Parimal Bal', '33. Description: Paid to Netflix', '34. Note: zepto protien bar | Description: Paid to zepto', '35. Description: Paid to Mr GANESH PRADEEP DALVI', '36. Note: Dinner | Description: Paid to Gandharva Restaurant', '37. Description: Paid to OM MILK DAIRY', '38. Note: Ola to Pune home | Description: Paid to Biradar Yogesh', '39. Note: Zudio Shopping | Description: Paid to Zudio Kumar Pacific Mall Pune Z140', '40. Note: Shopping for me dolly | Description: Paid to ADITYA BIRLA FASHION AND RETAIL', '41. Note: Train Pune to Amalner | Description: Paid to KUNAL RAJENDRA PATIL', '42. Note: Pantaloons Membership | Description: Paid to ADITYA BIRLA FASHION AND RETAIL', '43. Note: Parking | Description: Paid to KUMAR PARKING 2', '44. Note: Lunch at Khandesh Jankshan | Description: Paid to Hotel Khandesh Junction', '45. Note: Lunch | Description: Paid to CHIRP', '46. Note: Handwash Bottle | Description: Paid to MARKET 99', '47. Note: Payment for 25000867133749 | Description: Paid to Decathlon', '48. Note: Payment for 25000864755421 | Description: Paid to Decathlon', '49. Note: Levis Tshirts 2 | Description: Paid to LEVIS', '50. Note: Gini Dosa | Description: Paid to MADRAS CULINARY', '51. Note: scooty cover | Description: Paid to SHAKIRA YUSUF KHAN', '52. Note: Payment for 92415800 | Description: Paid to LENSKART', '53. Note: Eye drop | Description: Paid to Mr PRADNYA MALOJI GADEWAR', '54. Note: Eye Checkup | Description: Paid to Dr Manohar Dole Medical Foundation', '55. Note: Plants | Description: Paid to UNIVERSAL NURSERY SHOPI KRUSHI', '56. Note: Mogra | Description: Paid to SANDEEP DASHRATH BANKAR', '57. Note: Missal Pav 2 Sol Kadhi Taak | Description: Paid to JOGESHWARI MISAL', '58. Note: Air tyre | Description: Paid to MO GULAM', '59. Note: Petrol 2 ltr | Description: Paid to PATEL PETROLEUMS', '60. Note: Salt | Description: Paid to BALAJI TRADERS WHOLESALE', '61. Description: Paid to BALAJI TRADERS WHOLESALE', '62. Note: Paneer Yogurt | Description: Paid to SHIV KUMAR SINGH', '63. Note: Payment for 1157031085 | Description: Paid to WELLNESS FOREVER MH 2', '64. Note: Payment for 1157025850 | Description: Paid to WELLNESS FOREVER MH 2', '65. Note: Pani Puri | Description: Paid to MAYA GUPTA', '66. Note: Cutting | Description: Paid to RUPALI MAHESH JAGTAP', '67. Note: Batter 500g | Description: Paid to OMKAR DNYANESHWAR SONTAKKE', '68. Note: Paneer 250g | Description: Paid to SHIV KUMAR SINGH', '69. Note: Devendra Shinde | Description: Paid to DEVENDRA PRAMOD SHINDE', '70. Note: Blinkit Payment | Description: Paid to Blinkit', '71. Note: Paneer Yogurt | Description: Paid to SHIV KUMAR SINGH', '72. Description: Bill payment of Maharashtra State Electricity', '73. Note: Rent Feb 2026 | Description: Paid to POOJA KAKKULA', '74. Note: Ola to Pune home | Description: Paid to YOGESH LAHU SHINDE', '75. Note: Ola to Cafe Peter | Description: Paid to SIDHESHWAR PANDURANG PANCHAL', '76. Note: Ola to Pune home | Description: Paid to Mr RAVI SONERAO SONAWANE1', '77. Description: Paid to Mrs Priyanka Umesh', '78. Note: consultation | Description: Paid to Mrs Priyanka Umesh', '79. Note: Paneer Chingari | Description: Paid to Jaydev Parimal Bal', '80. Note: Mango Pickle | Description: Paid to CHAUBEY DHANANJAY', '81. Note: Lunch | Description: Paid to NEETI ENTERPRISES', '82. Note: Poha | Description: Paid to RUPALI RAVINDRA SHELAR', '83. Note: Uber to Pune home | Description: Paid to MOHAMMED MUJAHID', '84. Note: Dinner | Description: Paid to TRUPTI TUSHAR NIKAM', '85. Note: Bus to Pune | Description: Paid to REDBUS', '86. Note: Putane Biya | Description: Paid to Vijay Ashok Ramole', '87. Note: Ponga batata Masala pav | Description: Paid to BHUSHAN MOHAN PATIL', '88. Note: Jagruti and Rohit Gym Cricket | Description: Paid to NIKHIL PANDURANG MARNE', '89. Note: BhadePaySBZhd6tXCQSQvt | Description: Paid to Bhade Pay', '90. Note: Panchgani Trip | Description: Paid to YASH SANJAY GIDDIA', '91. Note: Panchgani Trip | Description: Paid to PRATIK SURESH MOHITE', '92. Note: Dinner | Description: Paid to SANDBHOR RAHUL SAMBHAJI', '93. Note: Salary Jan 2026 | Description: Paid to Mrs. Jadhav Jagruti Dilip', '94. Note: Uber to Sangamvadi Parking 1 | Description: Paid to SHETTY PRAJWAL NAGESH', '95. Note: Lunch | Description: Paid to ASHA SWEET AND SONPAPADI', '96. Note: Bus Pune to Nijampur | Description: Paid to REDBUS IN']


async def main() -> None:
    print(f"Testing Mistral with {len(SA)} transactions...\n")
    try:
        client = Mistral(api_key=os.environ["MISTRAL_API_KEY"])

        lines = []
        for i, description in enumerate(SA):
            parts = []
            note = ""
            if note and note.lower() not in ("paid via navi upi",
                                             "paid via navi", "null", ""):
                parts.append(f"Note: {note}")
            parts.append(f"Description: {description}")
            lines.append(f"{i + 1}. {' | '.join(parts)}")

        response = await client.chat.complete_async(
            model="mistral-small-latest",
            messages=[
                {"role": "system", "content": _SYSTEM},
                {"role": "user", "content": "\n".join(lines)},
            ],
            temperature=0,
            max_tokens=512,
        )

        raw = response.choices[0].message.content.strip()
        match = re.search(r'\[.*]', raw, re.DOTALL)
        if not match:
            raise ValueError(f"No JSON array in response: {raw[:200]}")
        cats = json.loads(match.group())
        results = [c if c in CATEGORIES else "Uncategorized" for c in cats]

        for desc, category in zip(SA, results):
            note = ""
            note_str = f" | Note: {note}" if note else ""
            print(f"  {desc}{note_str}  →  {category}")
        print("\nMistral is working!")
    except KeyError:
        print("\nError: MISTRAL_API_KEY not set in .env", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {e}", file=sys.stderr)
        sys.exit(1)


asyncio.run(main())
