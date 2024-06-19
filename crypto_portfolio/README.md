# Community Hass.io Add-ons: Crypto Portfolio

## About

Crypto Portfolio is an addon for Home Assistant to manage and track your cryptocurrency investments. With this addon, you can record your transactions, monitor the price evolution of each cryptocurrency, and visualize your overall portfolio performance.

## Installation

The installation of this add-on is straightforward and follows the same steps as other Hass.io add-ons.

1. Add this repository to your Hass.io instance.
2. Install the "Crypto Portfolio" add-on.
3. Start the "Crypto Portfolio" add-on.
4. Check the logs to ensure everything went well.

## Configuration

Example add-on configuration:

```json
{
  "update_interval": "5min",
  "currencies": ["bitcoin", "ethereum", "matic-network"]
}
