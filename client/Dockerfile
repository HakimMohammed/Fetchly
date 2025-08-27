# syntax=docker/dockerfile:1

FROM node:20-bullseye AS base

WORKDIR /app/client

# Install pnpm
RUN corepack enable && corepack prepare pnpm@9.12.0 --activate

# Install deps first for caching
COPY client/package.json client/pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile

# Build stage
FROM base AS build
COPY client/ .

# Build with env for API base URL (can be overridden at runtime for certain cases)
ARG NEXT_PUBLIC_API_BASE_URL=/api
ENV NEXT_PUBLIC_API_BASE_URL=$NEXT_PUBLIC_API_BASE_URL

RUN pnpm build

# Runtime image
FROM node:20-bullseye-slim AS runtime
WORKDIR /app/client

ENV NODE_ENV=production \
    HOST=0.0.0.0 \
    PORT=3000

# Copy only necessary artifacts
COPY --from=build /app/client/.next ./.next
COPY --from=build /app/client/public ./public
COPY --from=build /app/client/package.json ./package.json
COPY --from=build /app/client/next.config.mjs ./next.config.mjs

# Install production deps
RUN corepack enable && corepack prepare pnpm@9.12.0 --activate \
    && pnpm install --prod --frozen-lockfile

EXPOSE 3000
CMD ["pnpm", "start"]
