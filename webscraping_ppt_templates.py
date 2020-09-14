import time
import yaml
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


browser = webdriver.Chrome()
address = "https://24slides.com/templates/featured"
# address = "https://24slides.com/templates/most-popular"
# address = "https://24slides.com/templates/corporate-business-models"
# address = "https://24slides.com/templates/data-tables-graphs-charts"
# address = "https://24slides.com/templates/organization-planning"
# address = "https://24slides.com/templates/maps"
# address = "https://24slides.com/templates/other"

# A set of all the titles of the templates from the site, and a dict with the title as the key and link as value
template_titles = set()
title_link_dict = {}

browser.get(address)
time.sleep(1)

# containers for the template on the site
containers = browser.find_elements_by_tag_name("div.card")

# body of the page so that selenium can scroll down to load more templates
scroller = browser.find_element_by_tag_name("body")

#number of times to scroll down
no_of_pagedowns = 230
time.sleep(1)

filename = "template_links.csv"
f = open(filename, "w")
headers = "Name, Link\n"

f.write(headers)

# scrolls down and appends all the new containers to the list of containers
while no_of_pagedowns:
    scroller.send_keys(Keys.PAGE_DOWN)
    time.sleep(1.5)
    containers.append(browser.find_elements_by_tag_name("div.card"))
    no_of_pagedowns-=1
    print("Page-downs left: " + str(no_of_pagedowns))


# TODO separate these into methods
# for each container, if it's a list then iterate through the list to get each element and then take the title
# and the link and add it to the dictionary after checking that it's a new entry (may not need to check since it's a
# dict). If it's not a list then do the same thing without having to nested iterate
for container in containers:
    print("Entries so far: " + str(len(title_link_dict)))
    if isinstance(container,list):
        for c3 in container:
            try:
                if set.__contains__(template_titles, c3.text):
                    pass
                elif c3.text == "":
                    pass
                else:
                    set.add(template_titles, c3.text)

                    link = c3.find_element_by_css_selector('.card a').get_attribute('href')
                    trimmed_title = c3.text.splitlines()[0]
                    title_link_dict[trimmed_title] = link

                    csv_entry = '' + trimmed_title + ',' + link + '\n'
                    print("Entry: " + csv_entry)

            except Exception as e:
                print(e)

    else:

        try:
         if set.__contains__(template_titles,container.text):
            pass
         elif container.text == "":
             pass
         else:
            set.add(template_titles,container.text)

            link = container.find_element_by_css_selector('.card a').get_attribute('href')
            trimmed_title = container.text.splitlines()[0]
            title_link_dict[trimmed_title]=link

            csv_entry = '' + trimmed_title + ',' + link + '\n'
            print("Entry: " + csv_entry)

        except Exception as e:
            print(e)

# sorts the dictionary into a list of tuples ordering by the key
sorted_dict = sorted(title_link_dict.items(), key=lambda x:x)


for pair in sorted_dict:
    csv_entry = '' + pair[0] + ',' + pair[1] + '\n'
    f.write(csv_entry)


f.close()
print(len(containers))
print(len(template_titles))
print(len(title_link_dict))

print(yaml.dump(title_link_dict))

time.sleep(10)

browser.quit()