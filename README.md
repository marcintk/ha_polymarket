## Summary

Home Assistant integration to generate top news from [Polymarket](https://polymarket.com/) events and markets.

## Installation

This can be installed by copying all the files to `<config directory>/custom_components/polymarket/`.

## Configuration

Define scenes to be tracked and optional parameters in `configuration.yaml`.

```yaml
# Example of configuration.yaml
sensor:
  - platform: polymarket
    name: "Polymarket News"
    unique_id: polymarket_news
    refresh: 1
    limit: 5
    scenes:
      - name: general
      - name: nba
        tag_slug: nba
      - name: finance
        tag_slug: finance
      - name: politics
        tag_slug: politics
        exclude_tag_ids:
          - 972 # "slug": "tweets-markets"
```

The above will generate an entity with the id `sensor.polymarket_news` with top 5 news for the active scene. Each scene is selected, one by one, and is visible between refreshes (1min).

```
# Example of sensor attributes:
Domain: polymarket
Scene: nba
Url: http://gamma-api.polymarket.com/events?ascending=false&order=volume24hr&active=true&closed=false&limit=5&tag_slug=nba
QueryCount: 1
QueryFailed: 0
Timestamp: December 22, 2025 at 7:23:30 PM
Events:
  - active: true
    closed: false
    title: Fed decision in January?
    icon: https://polymarket-upload.s3.us-east-2.amazonaws.com/jerome+powell+glasses1.png
    volume: 49242293.04171
    volume24hr: 3634550.5518089994
    liquidity: 4494011.05495
    endsAt: '2026-01-28T00:00:00Z'
    updatedAt: '2025-12-23T01:19:24.841245Z'
    markets:
      - active: true
        closed: false
        title: No change
        volume: 6282263.15538
        volume24hr: 389282.69055500027
        liquidity: 248776.7973
        winPrice: 80.5
        updatedAt: '2025-12-23T01:17:52.984363Z'
      - active: true
        closed: false
        title: 25 bps decrease
        volume: 5861592.061526
        volume24hr: 332687.5343679997
        liquidity: 363563.2119
        winPrice: 17.5
        updatedAt: '2025-12-23T01:18:45.160663Z'
  - ...
```
