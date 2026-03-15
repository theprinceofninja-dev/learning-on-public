import os
import re
from dataclasses import dataclass


@dataclass
class Question:
    num: int
    text: str
    answers: list[str]


def parse_answer_key(text: str) -> dict[int, int]:
    m = re.search(r"مفتاح الإجابة:\s*(.*)\Z", text, flags=re.S)
    if not m:
        return {}
    key_block = m.group(1)
    key = {}
    for line in (l.strip() for l in key_block.splitlines()):
        if not line:
            continue
        mm = re.fullmatch(r"(\d+)\s*-\s*(\d+)", line)
        if mm:
            key[int(mm.group(1))] = int(mm.group(2))
    return key


def parse_quiz(text: str):
    lines = [l.strip() for l in text.splitlines()]
    lines = [l for l in lines if l]

    title = "\n".join(lines[:2]) if len(lines) >= 2 else "\n".join(lines)
    key = parse_answer_key(text)

    stop_idx = next(
        (i for i, l in enumerate(lines) if l.startswith("مفتاح الإجابة:")), len(lines)
    )
    body = lines[:stop_idx]

    sections = []
    cur_section = None

    i = 0
    while i < len(body):
        line = body[i]

        if line.startswith("القسم"):
            cur_section = {"title": line, "questions": []}
            sections.append(cur_section)
            i += 1
            continue

        qm = re.match(r"^(\d+)\.\s*(.*)$", line)
        if qm:
            qnum = int(qm.group(1))
            qtext = qm.group(2).strip()
            qtext = re.sub(r"؟\s*\d+$", "؟", qtext)

            answers = []
            j = i + 1
            while j < len(body) and len(answers) < 4:
                am = re.match(r"^\s*\d+\)\s*(.*)$", body[j])
                if not am:
                    break
                answers.append(am.group(0).strip())
                j += 1

            if cur_section is None:
                cur_section = {"title": "بدون قسم", "questions": []}
                sections.append(cur_section)

            cur_section["questions"].append(Question(qnum, qtext, answers))
            i = j
            continue

        i += 1

    return title, sections, key


import time

import pyautogui
import pyperclip


def copy_text_and_paste(text: str):
    pyperclip.copy(text)
    time.sleep(0.5)
    pyautogui.hotkey("ctrl", "v")


def choose_correct():
    pass


def get_mouse_location():
    x, y = pyautogui.position()
    print(f"Mouse location: X={x}, Y={y}")
    return (x, y)


def click_at_location(x, y, button="left", clicks=1, interval=0.1):
    pyautogui.moveTo(x, y, duration=0.2)  # Smooth movement

    pyautogui.click(x=x, y=y, button=button, clicks=clicks, interval=interval)
    print(f"Clicked at location: X={x}, Y={y}")


def click_send_button():
    click_at_location(1221, 852)


def click_text_area():
    click_at_location(862, 852)
    time.sleep(0.3)


#  X=1221, Y=852


def attach_a_poll():
    # Attach button X=1158, Y=854
    # Poll choice X=1094, Y=744

    click_at_image(img_path("attachment.png"))
    click_at_image(img_path("a_poll.png"))
    click_at_image(img_path("anonymous_voting.png"))
    click_at_image(img_path("quiz_mode.png"))


import time

import cv2
import numpy as np
import pyautogui
from PIL import Image


def click_image_from_several(image_path, confidence=0.8, click_index=0, timeout=10):
    print(f"Searching for ALL instances of: {image_path}")
    start_time = time.time()

    while time.time() - start_time < timeout:
        try:
            # Find ALL instances of the image
            locations = list(
                pyautogui.locateAllOnScreen(image_path, confidence=confidence)
            )

            if locations:
                print(f"Found {len(locations)} instance(s) of the image")

                # Check if the requested index exists
                if click_index < len(locations):
                    location = locations[click_index]
                    center_x = location.left + (location.width / 2)
                    center_y = location.top + (location.height / 2)

                    print(
                        f"Clicking instance #{click_index + 1} at: X={center_x}, Y={center_y}"
                    )

                    pyautogui.moveTo(center_x, center_y, duration=0.3)
                    time.sleep(0.1)
                    pyautogui.click()
                    return True
                else:
                    print(
                        f"Index {click_index} out of range. Found only {len(locations)} instances."
                    )
                    return False

        except Exception as e:
            print(f"Error: {e}")

        time.sleep(0.5)

    print(f"No instances found after {timeout} seconds")
    return False


def click_at_image(image_path, confidence=0.8, timeout=10):
    print(f"Searching for image: {image_path}")
    start_time = time.time()

    while time.time() - start_time < timeout:
        try:
            # Try to locate the image on screen
            location = pyautogui.locateOnScreen(image_path, confidence=confidence)

            if location:
                # Calculate center of the found image
                center_x = location.left + (location.width / 2)
                center_y = location.top + (location.height / 2)

                print(f"Found image at: X={center_x}, Y={center_y}")

                # Move to and click on the image
                pyautogui.moveTo(center_x, center_y, duration=0.3)
                time.sleep(0.3)
                pyautogui.click()
                time.sleep(0.3)
                print(f"Clicked on image: {image_path}")
                return True

        except pyautogui.ImageNotFoundException:
            pass  # Image not found in this attempt
        except Exception as e:
            print(f"Error: {e}")

        # Wait a bit before trying again
        time.sleep(0.5)

    print(f"Image '{image_path}' not found after {timeout} seconds")
    return False


def paste_question(question_text):
    click_at_image(img_path("ask_a_question.png"))
    copy_text_and_paste(question_text)


def print_formatted(
    title: str,
    sections,
    key: dict[int, int],
    continue_from_question: int = 0,
    continue_from_section: int = 0,
):
    if not continue_from_question and not continue_from_section:
        click_at_image(img_path("search_bar.png"))
        copy_text_and_paste("quizbot")
        time.sleep(0.5)
        click_at_image(img_path("quizbot_search_result.png"))
        click_at_image(img_path("start_button.png"))
        time.sleep(0.5)
        click_at_image(img_path("start_new_quiz.png"))

        for t in title.split("\n"):
            send_text(t)
            time.sleep(1)

    for s_index, sec in enumerate(sections, start=1):
        if continue_from_section and s_index < continue_from_section:
            continue
        send_text(sec["title"])

        for q_index, q in enumerate(sec["questions"], start=1):
            print("Checking what to do with question number", q.num)
            if not continue_from_section:
                if continue_from_question and q_index < continue_from_question:
                    continue
            attach_a_poll()
            correct = key.get(q.num)
            paste_question(f"{q.num}. {q.text}")

            for a in q.answers:
                am = re.match(r"^(\d+)\)", a)
                anum = int(am.group(1)) if am else None
                click_at_image(img_path("add_an_option.png"))
                time.sleep(0.5)
                copy_text_and_paste(a)
                time.sleep(0.5)
                if correct is not None and anum == correct and anum is not None:
                    click_image_from_several(
                        img_path("correct_circle.png"), click_index=anum - 1
                    )
            click_at_image(img_path("create_button.png"))
            time.sleep(0.5)


def img_path(img_name):
    return os.path.join(os.path.dirname(__file__), img_name)


def send_text(title):
    click_text_area()
    copy_text_and_paste(title)
    click_send_button()


if __name__ == "__main__":
    INPUT_TEXT = r"""بنك الأسئلة الشامل: الصناعات البتروكيميائية القائمة على الإيثيلين (C2)
    عدد الأسئلة: 50 سؤالاً | المحتوى: الحفازات، شروط التفاعل، الآليات، والمنتجات.
    
القسم الأول: الحفازات (Catalysts)
1. ما هو الحفاز الوحيد القادر على تشكيل حلقة "الإيبوكسيد" في عملية الأكسدة المباشرة للإيثيلين؟ 1
1) النحاس (Cu)
2) الفضة على الألومينا (Ag/Alumina)
3) الحديد (Fe)
4) البلاتين (Pt)

2. ما هو نظام الحفاز المتجانس المستخدم في "عملية فاكر" (Wacker) لإنتاج الأسيت ألدهيد؟ 2
1) PdCl_2 + CuCl_2
2) TiCl_4 + Al(Et)_3
3) Fe_2O_3
4) Ni(CO)_4

3. في تفاعل "الأوكسي كلورة" لإنتاج (EDC)، ما هو الحفاز المستخدم وفي أي طور؟ 3
1) كلوريد الحديد الصلب
2) كلوريد النحاس (CuCl_2) المذاب في سائل
3) حمض الفوسفور الغازي
4) الفضة على دعامة صلبة

4. ما هو الحفاز المستخدم في تفاعل "ريتي" (Reppe) لإنتاج حمض البروبيونيك مباشرة؟ 4
1) كربونيل الكوبالت
2) هيدرو هاليد كربونيل النيكل (Ni(CO)_4)
3) أكسيد الفاناديوم
4) الزيوليت

5. ما نوع الحفازات المستخدمة في عملية "ألفول" (ALFOL) لإنتاج الكحولات الخطية؟ 5
1) حفازات زيغلر (Al(R)_3)
2) حفازات فريدل-كرافتس
3) حفازات الأكسدة
4) حفازات حمضية سائلة

6. عند إنتاج الإيثانول بالإماهة المباشرة، ما هو الحفاز المستخدم؟ 6
1) حمض الكبريت السائل
2) حمض الفوسفور المحمل على تربة دياتوميت
3) أكسيد النحاس
4) كلوريد الزئبق

7. ما هو الحفاز المستخدم لتحويل الأسيت ألدهيد إلى "حمض الخل" في الطور السائل؟ 7
1) خلات المنغنيز
2) خلات الفينيل
3) كلوريد البالاديوم
4) حمض الكبريت

8. في عملية إنتاج "1,3-بروبان ديول"، ما المادة المعززة المضافة لحفاز كربونيل الكوبالت؟ 8
1) حمض الخل
2) بوتيل البيريدين
3) الأمونيا
4) الماء

9. ما هو الحفاز المستخدم لأكسدة البروبيلين إلى "أسيتون" عند 110 مئوية؟ 9
1) CuCl_2 محمل على PdCl_2
2) Ag على الألومينا
3) H_3PO_4
4) FeCl_3

10. ما هو الحفاز المستخدم في تفاعل "أوكسو" لإنتاج "البوتير ألدهيد" من البروبيلين؟ 10
1) النيكل
2) الروديوم (Rhodium)
3) الحديد
4) التيتانيوم

11. ما هو الحفاز المستخدم لإنتاج "الكيتين" بالتفكيك الحراري لحمض الخل؟ 11
1) حمض الفوسفور (H_3PO_4)
2) حمض الكبريت
3) هيدروكسيد الصوديوم
4) أكسيد الزنك

القسم الثاني: شروط التفاعل (Conditions: T & P)
12. كم تبلغ درجة الحرارة والضغط في المفاعل الأنبوبي لإنتاج أكسيد الإيثيلين؟ 12121212
1) 500°C و 1 atm
2) 200-300°C و 10-20 atm
3) 100°C و 50 atm
4) 50°C و 5 atm+1

13. لماذا يفضل إجراء "الكلورة المباشرة" للإيثيلين عند درجات حرارة منخفضة؟ 13
1) لزيادة سرعة التفاعل
2) لضمان انتقائية عالية وتجنب النواتج الثانوية
3) لأن الحفاز يتفكك بالحرارة
4) لتقليل تكلفة الطاقة فقط

14. ما هي درجة الحرارة اللازمة لتكسير (EDC) حرارياً لإنتاج فينيل كلوريد (VCM)؟ 14
1) 100°C
2) 250°C
3) حوالي 500°C
4) 1000°C

15. في تفاعل إنتاج "خلات الفينيل" بالطور البخاري، ما هي الشروط المثلى؟ 15
1) 160°C وضغط 5-10 atm
2) 300°C وضغط جوي
3) 50°C وضغط عالٍ
4) 600°C وضغط مفرغ

16. ما هو الضغط المطلوب لتفاعل "الهيدروفورميل" باستخدام حفاز الكوبالت؟ 16
1) 1-5 psi
2) 50-100 psi
3) 1500-4500 psi
4) ضغط جوي عادي

17. ما هي نسبة التحويل (Conversion) المقبولة للإيثيلين في أكسدة خلات الفينيل لضمان الأمان؟ 17
1) 90-95%
2) 50%
3) 10-15%
4) 100%

18. ما هو الضغط المستخدم في تفاعل "الكربلة التأكسدية" لإنتاج حمض الأكريليك؟ 18
1) 7 atm
2) 100 atm
3) 1 atm
4) 50 atm

19. كم يبلغ وقت التفاعل في مرحلة "البلمرة" لعملية (ALFOL) لإنتاج كحول C_{12}؟ 19
1) 10 دقائق
2) حوالي 140 دقيقة
3) 24 ساعة
4) 5 ساعات

20. ما هي درجة الحرارة في "العملية أحادية المرحلة" لإنتاج الأسيت ألدهيد (فاكر)؟ 20
1) 130°C
2) 300°C
3) 25°C
4) 500°C

21. ما هو تركيز حمض الكبريت المستخدم لامتصاص البروبيلين لإنتاج الإيزوبروبانول؟ 21
1) 98%
2) 85%
3) 50%
4) 10%

22. ما هي نسبة التحويل في التذكرة الواحدة (Per pass) لتكسير EDC؟ 22
1) 90%
2) 100%
3) 50%
4) 10%

القسم الثالث: الآليات والتفاعلات (Mechanisms)
23. ما نوع التفاعل في الخطوة الثانية من عملية فاكر (Pd^0 إلى Pd^{+2} بوجود النحاس)؟ 23
1) أكسدة وإرجاع (Redox)
2) بلمرة
3) حلمهة
4) إضافة

24. ما هي آلية تفاعل "الكلورة المباشرة" للإيثيلين بوجود حفاز FeCl_3؟ 24
1) جذرية (Radical)
2) أيونية (Ionic / Electrophilic)
3) تكاثف
4) حذف

25. ما هي آلية تفاعل الكلورة المباشرة في "غياب" الحفاز؟ 25
1) أيونية
2) جذرية (Free Radical)
3) تناسقية
4) تبادل

26. ما هي مشكلة تفاعل "الإيثوكسيل" (إضافة EO للكحولات) الرئيسية؟ 26
1) التفاعل ماص للحرارة
2) التفاعل ناشر للحرارة بشدة (خطر الهروب الحراري)
3) التفاعل لا يحدث إلا بضغط عالٍ جداً
4) التفاعل ينتج غازات سامة

27. كيف تتم ديمرة الإيثيلين إلى "بوتين-1" وفق الآلية القديمة؟ 27
1) آلية جذرية حرة
2) تشكل "حلقة معدنية" (Metallacycle)
3) تكاثف ألدولي
4) هدرجة مباشرة

28. ما هو الفرق في سرعة تفاعل الكحولات الأولية مع (EO) مقارنة بالثانوية؟ 28
1) السرعة متساوية
2) الثانوية أسرع بمرتين
3) الأولية أسرع بـ 10-30 ضعفاً
4) الأولية أبطأ

29. ما هو المركب الوسطي الذي يتشكل في آلية تفاعل "ريتي" (Reppe)؟ 29
1) جذر ميثيل حر
2) معقد باي حلقي (pi-complex)
3) أيون كاربونيوم
4) أكسيد النيكل

30. ما هي الغاية من استخدام بخار الماء في عملية إماهة الإيثيلين بحمض الكبريت (الطريقة القديمة)؟ 30
1) تبريد التفاعل
2) حلمهة الإستر المتشكل (Et-O-SO_3H) وتمديده
3) زيادة الضغط
4) كعامل مؤكسد

القسم الرابع: المنتجات والاستخدامات (Products & Uses)
31. ما هي نسبة (الماء : أكسيد الإيثيلين) لإنتاج (MEG) بانتقائية عالية؟ 31
1) 1:1
2) 10:1
3) 1:10
4) 50:1

32. ما هو الاستخدام الرئيسي لمركب "الكمبرلان" (ثنائي إيثانول كوكو أمي4)؟ 32
1) وقود للسيارات
2) معزز للرغوة ورافع للزوجة في الشامبو
3) سماد زراعي
4) مذيب للدهانات

33. لماذا يضاف "ثنائي فينيل البنزوكينون" إلى مونومر (VCM) النقي؟ 33
1) لتسريع البلمرة
2) كمانع للبلمرة التلقائية أثناء النقل
3) لتحسين اللون
4) لزيادة القابلية للاشتعال

34. ما هما المركبان المستخدمان لإنتاج "البنتا إريتريتول"؟ 34
1) الأسيت ألدهيد + الفورم ألدهيد
2) الأسيتون + الإيثانول
3) الإيثيلين + الأكسجين
4) حمض الخل + الميثانول

35. لماذا توقفت طريقة "الكلورهيدرين" القديمة لإنتاج أكسيد الإيثيلين؟ 353535
1) لأنها بطيئة جداً
2) بسبب استهلاك الكلور وتحوله لملح (CaCl2) قليل القيمة
3) لأنها تحتاج ضغطاً عالياً جداً
4) لأنها تنتج غازات دفيئة فقط+1

36. عند هيدروفورميل "البروبيلين"، ما هي نسبة النواتج (نظامي : إيزو)؟ 36
1) 100% نظامي
2) 50% نظامي : 50% إيزو
3) 60% نظامي : 40% إيزو
4) 95% إيزو

37. ما هو الغاز المعاد تدويره من عملية تكسير (EDC) إلى وحدة الأوكسي كلورة؟ 37
1) غاز الكلور (Cl_2)
2) غاز كلوريد الهيدروجين (HCl)
3) غاز الهيدروجين (H_2)
4) غاز الإيثيلين
38. ما الناتج الرئيسي من أكسدة "3-بيكولين" في الطور السائل؟ 38
1) بيريدين
2) حمض النيكوتين
3) نيكوتين أميد
4) أنيلين

39. كم تبلغ انتقائية أكسيد الإيثيلين في طريقة الأكسدة المباشرة؟ 39
1) 50%
2) 99%
3) 90%
4) 10%

40. كم يبلغ العمر الافتراضي لحفاز الفضة في إنتاج EO؟ 40
1) 6 أشهر
2) 3-5 سنوات
3) 10 سنوات
4) 20 سنة

41. ما هو المركب الناتج عن تكاثف "البوتير ألدهيد" ثم هدرجته؟ 41
1) 1-بوتانول
2) 2-إيثيل هكسانول (أوكتانول)
3) بروبانول
4) ميثانول

42. ما هي المادة الملدنة (Plasticizer) المنتجة من تفاعل حمض الفيتاليك مع 2-إيثيل هكسانول؟ 42
1) PVC
2) DOP (ثنائي أوكتيل الفيتالات)
3) PET
4) PS

43. ما هو استخدام حمض البروبيونيك الناتج عن تفاعل ريتي؟ 43
1) وقود طائرات
2) حافظ للحبوب (ضد الفطريات والبكتيريا)
3) مادة متفجرة
4) صناعة البلاستيك المقوى

44. ما هو الناتج الثانوي "النظيف" عند أكسدة 3-بيكولين بالطور الغازي؟ 44
1) CO_2
2) NO_x
3) الماء (H_2O)
4) الميثان

45. ماذا ينتج عن حلمهة "3-سيانو بيريدين" في وسط قلوي (pH > 7)؟ 45
1) حمض النيكوتين فوراً
2) نيكوتين أميد
3) بيريدين
4) أمونيا فقط

46. ما هو الاستخدام الصناعي لمركب "بركلورو إيثيلين"؟ 46
1) تنظيف جاف (Dry Cleaning) وإزالة الشحوم
2) سماد
3) مادة حافظة للأغذية
4) وقود

47. كيف يؤثر إدخال زمر الإيثوكسيل (EO) على قيمة HLB للمركب؟ 47
1) يخفضها
2) يرفع قيمة HLB (يزيد القطبية)
3) لا يؤثر
4) يجعلها صفر

48. ماذا ينتج عن الأكسدة الأمونية لمركب 3-ميثيل البيريدين؟ 48
1) 3-سيانو بيريدين
2) 2-بيكولين
3) حمض الخل
4) فينيل بيريدين
49. ما الفرق في انتقائية تفاعل "أوكسو" بين الإيزوبوتيلين والبروبيلين؟ 49
1) كلاهما يعطي 50% خليط
2) الإيزوبوتيلين يعطي انتقائية عالية (95% إيزو فالير ألدهي4)
3) البروبيلين يعطي منتجاً واحداً فقط
4) الإيزوبوتيلين لا يتفاعل

50. ما هو الهدف من إضافة الأوليفينات (مثل بوتين-1) أثناء بلمرة الإيثيلين؟ 50
1) لخفض التكلفة فقط
2) لإنتاج بولي إيثيلين منخفض الكثافة الخطي (LLDPE) وتحسين الخواص الميكانيكية
3) لإنتاج بولي إيثيلين عالي الكثافة جداً
4) لتغيير لون البلاستيك

مفتاح الإجابة:
1-2
2-1
3-2
4-2
5-1
6-2
7-1
8-2
9-1
10-2
11-1
12-2
13-2
14-3
15-1
16-3
17-3
18-1
19-2
20-1
21-2
22-3
23-1
24-2
25-2
26-2
27-2
28-3
29-2
30-2
31-2
32-2
33-2
34-1
35-2
36-3
37-2
38-2
39-3
40-2
41-2
42-2
43-2
44-3
45-2
46-1
47-2
48-1
49-2
50-2
"""
    title, sections, key = parse_quiz(INPUT_TEXT)
    print_formatted(
        title, sections, key, continue_from_question=12, continue_from_section=2
    )
