FROM golang:1.21-alpine AS builder

WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download

COPY src/ ./src/
RUN CGO_ENABLED=0 GOOS=linux go build -o payment-service ./src/

FROM alpine:latest
RUN apk --no-cache add ca-certificates curl
WORKDIR /root/

# Add non-root user
RUN adduser -D -s /bin/sh appuser
USER appuser

COPY --from=builder /app/payment-service .

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8080/health || exit 1

CMD ["./payment-service"]