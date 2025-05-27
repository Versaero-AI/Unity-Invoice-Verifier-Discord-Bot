# Inbora Verifier Bot

A Discord bot designed to verify Unity Asset Store invoices and assign roles to verified users. This bot includes both prefix commands (`+`) and slash commands (`/`), with administrative tools for managing verified invoices.

## Features
- Verify Unity Asset Store invoices using an API.
- Assign roles to users upon successful verification.
- Admin commands to manage verified invoices (list, delete, update, count).
- Restrict bot usage to a specific server.
- Customizable responses for user mentions.
- Persistent storage using SQLite.

## Setup
1. **Clone the repository**:
   ```bash
   git clone https://github.com/Versaero-AI/Unity-Invoice-Verifier-Discord-Bot
   cd Unity-Invoice-Verifier-Discord-Bot
