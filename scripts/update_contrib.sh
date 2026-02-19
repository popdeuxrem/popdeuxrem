#!/bin/bash
curl -s "https://github.com/popdeuxrem/popdeuxrem/graphs/contribution?type=calendar" > temp.html
echo "Placeholder contrib graph updated" > assets/contrib-graph.svg
rm temp.html
git add assets/contrib-graph.svg
git commit -m "chore: update contrib graph $(date +%Y-%m-%d)"
git push
