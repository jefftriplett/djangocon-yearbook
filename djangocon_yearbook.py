"""

Quick attempt to extract speakers and talks from every DjangoCon US.

To install requirements:

    pip install grab rich typer

Goals:

- [x] Extract speakers and talks from every DjangoCon US. (DONE)
- [x] Store extracted information in a useful format (mostly DONE)
- [ ] Process information into an app
- [ ] Expand for DjangoCon EU + AU

"""

import csv
import typer

from grab import Grab
from pathlib import Path
from rich import print


app = typer.Typer()

# ----------------------------------------------------------------
# our supporting utils...
# ----------------------------------------------------------------


def build_speaker_page(filename, ignore_speaker=False):
    talks = csv_to_list(filename)
    for talk in talks:
        speaker = talk["speaker"]
        talk_name = talk["talk_name"]
        if len(speaker) and len(talk_name) or ignore_speaker:
            print(
                "1. [{speaker}: **{talk_name}**]({talk_url})".format(
                    speaker=speaker,
                    talk_name=talk_name,
                    talk_url=talk["talk_url"],
                )
            )


def csv_to_list(filename, delimiter=","):
    with Path(filename).open() as f:
        rows = list(csv.DictReader(f, delimiter=delimiter))
        return rows
    return []


def write_csv(filename, rows):
    with Path(filename).open("w") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        writer.writerow(
            [
                "conference",
                "year",
                "start_time",
                "speaker",
                "talk_name",
                "talk_url",
                "video_url",
                "slides_url",
            ]
        )
        for row in rows:
            writer.writerow(
                [
                    row.get("conference"),
                    row.get("year"),
                    row.get("start_time"),
                    row.get("speaker"),
                    row.get("talk_name"),
                    row.get("talk_url"),
                    row.get("video_url"),
                    row.get("slides_url"),
                ]
            )


# ----------------------------------------------------------------
# our apps commands
# ----------------------------------------------------------------


@app.command()
def build_csv():
    print("## 2015")
    build_speaker_page("csv/djangocon-us-2015.csv")
    print()
    print("## 2014")
    build_speaker_page("csv/djangocon-us-2014.csv")
    print()
    print("## 2013")
    build_speaker_page("csv/djangocon-us-2013.csv")
    print()
    print("## 2012")
    build_speaker_page("csv/djangocon-us-2012.csv")
    print()
    print("## 2011")
    build_speaker_page("csv/djangocon-us-2011.csv")
    print()
    print("## 2010")
    build_speaker_page("csv/djangocon-us-2010.csv", ignore_speaker=True)
    print()
    print("## 2009")
    build_speaker_page("csv/djangocon-us-2009.csv")
    print()
    print("## 2008")
    build_speaker_page("csv/djangocon-us-2008.csv")


@app.command()
def fetch_all():
    try:
        fetch_2008()
    except Exception as exception:
        print(exception)

    try:
        fetch_2009()
    except Exception as exception:
        print(exception)

    try:
        fetch_2010()
    except Exception as exception:
        print(exception)

    try:
        fetch_2011()
    except Exception as exception:
        print(exception)

    try:
        fetch_2012()
    except Exception as exception:
        print(exception)

    try:
        fetch_2013()
    except Exception as exception:
        print(exception)

    try:
        fetch_2014()
    except Exception as exception:
        print(exception)

    try:
        fetch_2015()
    except Exception as exception:
        print(exception)


@app.command()
def fetch_2008():
    url = "http://web.archive.org/web/20090217112815id_/http://djangocon.org/program"
    grab = Grab()
    grab.go(url)

    """
    <tr class="odd first">
        <td>9:00am - 9:50am</td>
        <td>Building 40</td>
        <td>-</td>
        <td>Doors Open/Registration</td>
    </tr>
    <tr class="even">
        <td>10:00am - 10:10am</td>
        <td>Track 1</td>
        <td>Robert Lofthouse</td>
        <td>Keynote: Chairman's Opening Statement</td>
    </tr>
    """
    data = []
    rows = [item for item in grab.doc("//table/tbody/tr")]
    for row in rows:
        print(f"[blue]{row.text()}[/blue]")
        talk = row.select("td")
        if talk.exists():
            start_time = talk[0].text()
            speaker = talk[2].text()
            talk_name = talk[3].text()

            print(f"[yellow]{talk.text()}[/yellow]")
            print("start_time: {0}".format(start_time))
            print("speaker: {0}".format(speaker))
            print("talk name: {0}".format(talk_name))
            # print(u'talk url: {0}'.format(talk_url))
            print()
            data.append(
                {
                    "conference": "djangocon-us",
                    "year": "2008",
                    "start_time": start_time,
                    "speaker": speaker,
                    "talk_name": talk_name,
                    "talk_url": "",
                }
            )

    write_csv("csv/djangocon-us-2008.csv", data)


@app.command()
def fetch_2009():
    url = "http://web.archive.org/web/20100428054846id_/http://www.djangocon.org/2009/conference/schedule/"
    grab = Grab()
    grab.go(url)

    """
    <tr>
        <td class="time">8:00 - 18:00</td>
        <td class="talk colspan="2"><p>Registration opens for the rest of the day.</p></td>
    </tr>
    <tr class="even">
        <td class="time">9:00</td>
        <td class="talk" colspan="2"><p>Chairman's Opening Remarks & Introduction from the Fake Jacob Kaplan-Moss</p></td>
    </tr>
    """

    data = []
    rows = [item for item in grab.doc("//table/tbody/tr")]
    for row in rows:
        print(f"[blue]{row.text()}[/blue]")

        start_time = row.select("td")
        if start_time.exists():
            start_time = start_time.text()
        else:
            start_time = ""

        print(f"[blue]{row.text()}[/blue]")

        talks = row.select("td")[1:]
        for talk in talks:
            speaking_info = talk.select("p")

            if speaking_info.exists() and len(speaking_info) > 1:
                speaker = speaking_info[1].text()
                talk_name = speaking_info[0].text()

                print(f"[yellow]{talk.text()}[/yellow]")
                print("start_time: {0}".format(start_time))
                print("speaker: {0}".format(speaker))
                print("talk name: {0}".format(talk_name))
                # print(u'talk url: {0}'.format(talk_url))
                print()

                data.append(
                    {
                        "conference": "djangocon-us",
                        "year": "2009",
                        "start_time": start_time,
                        "speaker": speaker,
                        "talk_name": talk_name,
                        "talk_url": "",
                    }
                )

    write_csv("csv/djangocon-us-2009.csv", data)


@app.command()
def fetch_2010():
    url = "http://web.archive.org/web/20101005140539id_/http://djangocon.us/schedule/"
    grab = Grab()
    grab.go(url)

    data = []
    rows = [item for item in grab.doc("//table/tr")]
    for row in rows:
        start_time = row.select("td")
        if start_time.exists():
            start_time = start_time.text()
        else:
            start_time = ""

        print(f"[blue]{row.text()}[/blue]")

        talks = row.select("td")[1:]
        for talk in talks:
            speaker = talk.select('td[contains(@class, "speaker")]')

            if speaker.exists():
                speaker = speaker.text().strip()
            else:
                speaker = ""

            anchor = talk.select("a")
            if anchor.exists():
                talk_name = anchor.text()
                talk_url = "http://web.archive.org/web/20101005140539id_/http://djangocon.us/{0}".format(
                    anchor.attr("href", "")
                )
            else:
                talk_name = ""
                talk_url = ""

            print(f"[yellow]{talk.text()}[/yellow]")
            print("start_time: {0}".format(start_time))
            print("speaker: {0}".format(speaker))
            print("talk name: {0}".format(talk_name))
            print("talk url: {0}".format(talk_url))
            print()

            data.append(
                {
                    "conference": "djangocon-us",
                    "year": "2010",
                    "start_time": start_time,
                    "speaker": speaker,
                    "talk_name": talk_name,
                    "talk_url": talk_url,
                }
            )

    write_csv("csv/djangocon-us-2010.csv", data)


@app.command()
def fetch_2011():
    url = "http://2011.djangocon.us/schedule/"
    grab = Grab()
    grab.go(url)

    data = []
    rows = [item for item in grab.doc("//table/tr")]
    for row in rows:
        start_time = row.select('td[contains(@class, "time")]')
        if start_time.exists():
            start_time = start_time.text()
        else:
            start_time = ""

        print(f"[blue]{row.text()}[/blue]")

        talks = row.select("td")[1:]
        for talk in talks:
            speaker = talk.select('div[contains(@class, "speaker")]')

            if speaker.exists():
                speaker = speaker.text().strip()
            else:
                speaker = ""

            anchor = talk.select('div[contains(@class, "title")]/a')
            if anchor.exists():
                talk_name = anchor.text()
                talk_url = "http://2011.djangocon.us/{0}".format(
                    anchor.attr("href", "")
                )
            else:
                talk_name = ""
                talk_url = ""

            print(f"[yellow]{talk.text()}[/yellow]")
            print("start_time: {0}".format(start_time))
            print("speaker: {0}".format(speaker))
            print("talk name: {0}".format(talk_name))
            print("talk url: {0}".format(talk_url))
            print()

            data.append(
                {
                    "conference": "djangocon-us",
                    "year": "2011",
                    "start_time": start_time,
                    "speaker": speaker,
                    "talk_name": talk_name,
                    "talk_url": talk_url,
                }
            )

    write_csv("csv/djangocon-us-2011.csv", data)


@app.command()
def fetch_2012():
    url = "http://2012.djangocon.us/schedule/"
    grab = Grab()
    grab.go(url)

    data = []
    rows = [item for item in grab.doc("//table/tr")]
    for row in rows:
        start_time = row.select('td[contains(@class, "time")]')
        if start_time.exists():
            start_time = start_time.text()
        else:
            start_time = ""

        print(f"[blue]{row.text()}[/blue]")

        talks = row.select("td")[1:]
        for talk in talks:
            speaker = talk.select('div[contains(@class, "speaker")]')

            if speaker.exists():
                speaker = speaker.text().strip()
            else:
                speaker = ""

            anchor = talk.select('div[contains(@class, "title")]/a')
            if anchor.exists():
                talk_name = anchor.text()
                talk_url = "http://2012.djangocon.us/{0}".format(
                    anchor.attr("href", "")
                )
            else:
                talk_name = ""
                talk_url = ""

            print(f"[yellow]{talk.text()}[/yellow]")
            print("start_time: {0}".format(start_time))
            print("speaker: {0}".format(speaker))
            print("talk name: {0}".format(talk_name))
            print("talk url: {0}".format(talk_url))
            print()

            data.append(
                {
                    "conference": "djangocon-us",
                    "year": "2012",
                    "start_time": start_time,
                    "speaker": speaker,
                    "talk_name": talk_name,
                    "talk_url": talk_url,
                }
            )

    write_csv("csv/djangocon-us-2012.csv", data)


@app.command()
def fetch_2013():
    url = "https://web.archive.org/web/20131022134635id_/http://djangocon.us/schedule/"
    grab = Grab()
    grab.go(url)

    data = []
    rows = [item for item in grab.doc("//table/tbody/tr")]
    for row in rows:
        start_time = row.select('td[contains(@class, "time")]')
        if start_time.exists():
            start_time = start_time.text()
        else:
            start_time = ""

        print(f"[blue]{row.text()}[/blue]")

        talks = row.select("td")[1:]
        for talk in talks:
            speaker = talk.select('span[contains(@class, "speaker")]')

            if speaker.exists():
                speaker = speaker.text().strip()
            else:
                speaker = ""

            anchor = talk.select('span[contains(@class, "title")]/a')
            if anchor.exists():
                talk_name = anchor.text()
                talk_url = "http://2012.djangocon.us/{0}".format(
                    anchor.attr("href", "")
                )
            else:
                talk_name = ""
                talk_url = ""

            print(f"[yellow]{talk.text()}[/yellow]")
            print("start_time: {0}".format(start_time))
            print("speaker: {0}".format(speaker))
            print("talk name: {0}".format(talk_name))
            print("talk url: {0}".format(talk_url))
            print()

            data.append(
                {
                    "conference": "djangocon-us",
                    "year": "2013",
                    "start_time": start_time,
                    "speaker": speaker,
                    "talk_name": talk_name,
                    "talk_url": talk_url,
                }
            )

    write_csv("csv/djangocon-us-2013.csv", data)


@app.command()
def fetch_2014():
    url = "http://2014.djangocon.us/schedule/"
    g = Grab()
    g.go(url)

    data = []
    talks = [item for item in g.doc("//table/tbody/tr")]
    for talk in talks:
        row = talk.select("td")
        anchor = row.select("p/a")
        start_time = row.select("p").text()
        speaker = row.select('p[contains(@class, "speaker")]')
        if speaker.exists():
            speaker = speaker.text()
        else:
            speaker = ""

        print(row.text())
        if anchor.exists():
            talk_name = anchor.text()
            talk_url = "https://2015.djangocon.us/{0}".format(anchor.attr("href", ""))
        else:
            talk_name = ""
            talk_url = ""

        print(f"[blue]{talk.text()}[/blue]")
        print("start_time: {0}".format(start_time))
        print("speaker: {0}".format(speaker))
        print("talk name: {0}".format(talk_name))
        print("talk url: {0}".format(talk_url))
        print()

        data.append(
            {
                "conference": "djangocon-us",
                "year": "2014",
                "start_time": start_time,
                "speaker": speaker,
                "talk_name": talk_name,
                "talk_url": talk_url,
            }
        )

    write_csv("csv/djangocon-us-2014.csv", data)


@app.command()
def fetch_2015():
    url = "http://2015.djangocon.us/schedule/general-sessions/"
    g = Grab()
    g.go(url)

    data = []
    talks = [item for item in g.doc("//table/tbody/tr")]
    for talk in talks:
        rows = talk.select("td")
        for row in rows:
            anchor = row.select('p[contains(@class, "start-time")]/a')
            start_time = row.select("p").text()
            speaker = row.select('p[contains(@class, "speaker")]')
            if speaker.exists():
                speaker = speaker.text()
            else:
                speaker = ""

            print(row.text())
            if anchor.exists():
                talk_name = anchor.text()
                talk_url = "https://2015.djangocon.us{0}".format(
                    anchor.attr("href", "")
                )
            else:
                talk_name = ""
                talk_url = ""

            print(f"[blue]{talk.text()}[/blue]")
            print("start_time: {0}".format(start_time))
            print("speaker: {0}".format(speaker))
            print("talk name: {0}".format(talk_name))
            print("talk url: {0}".format(talk_url))
            print()

            data.append(
                {
                    "conference": "djangocon-us",
                    "year": "2015",
                    "start_time": start_time,
                    "speaker": speaker,
                    "talk_name": talk_name,
                    "talk_url": talk_url,
                }
            )

    write_csv("csv/djangocon-us-2015.csv", data)


if __name__ == "__main__":
    app()
