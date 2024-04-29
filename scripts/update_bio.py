import datetime

# Calculate current date and day name
current_date = datetime.datetime.now()
day_name = current_date.strftime('%A')
date_str = current_date.strftime('%d of %B of %Y')

# Create a bio content with context and emojis
bio_content = (
    f"👋 On this {day_name}, {date_str}, I am working as a Mobile Developer "
    f"💼📱 @miniclip and advancing my PhD studies in Technology 👨🏻‍💻🎓 @iade-pt. "
    f"👾 Passionate about game development and leveraging tech for creative solutions!"
)

print(bio_content)
