.class public final Lpmsj/work/main/w;
.super Ljava/lang/Object;


# static fields
.field public static a:Lpmsj/work/main/w;


# instance fields
.field public b:Ljava/util/Vector;


# direct methods
.method public constructor <init>()V
    .locals 1

    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    new-instance v0, Ljava/util/Vector;

    invoke-direct {v0}, Ljava/util/Vector;-><init>()V

    iput-object v0, p0, Lpmsj/work/main/w;->b:Ljava/util/Vector;

    return-void
.end method

.method public static a()Lpmsj/work/main/w;
    .locals 1

    sget-object v0, Lpmsj/work/main/w;->a:Lpmsj/work/main/w;

    if-nez v0, :cond_0

    new-instance v0, Lpmsj/work/main/w;

    invoke-direct {v0}, Lpmsj/work/main/w;-><init>()V

    sput-object v0, Lpmsj/work/main/w;->a:Lpmsj/work/main/w;

    :cond_0
    sget-object v0, Lpmsj/work/main/w;->a:Lpmsj/work/main/w;

    return-object v0
.end method

.method public static a(BIIII)V
    .locals 2

    new-instance v0, La/c/r;

    invoke-direct {v0}, La/c/r;-><init>()V

    const/16 v1, 0x57b

    invoke-virtual {v0, v1}, La/c/r;->a(I)V

    invoke-virtual {v0, p0}, La/c/r;->b(I)V

    invoke-virtual {v0, p1}, La/c/r;->d(I)V

    invoke-virtual {v0, p2}, La/c/r;->d(I)V

    invoke-virtual {v0, p3}, La/c/r;->d(I)V

    invoke-virtual {v0, p4}, La/c/r;->d(I)V

    sget-object v1, Lpmsj/work/main/e;->a:Lpmsj/work/main/i;

    invoke-virtual {v0}, La/c/r;->a()[B

    move-result-object v0

    invoke-virtual {v1, v0}, Lpmsj/work/main/i;->b([B)V

    return-void
.end method

.method public static a(IB)V
    .locals 2

    new-instance v0, La/c/r;

    invoke-direct {v0}, La/c/r;-><init>()V

    invoke-virtual {v0, p0}, La/c/r;->a(I)V

    invoke-virtual {v0, p1}, La/c/r;->b(I)V

    sget-object v1, Lpmsj/work/main/e;->a:Lpmsj/work/main/i;

    invoke-virtual {v0}, La/c/r;->a()[B

    move-result-object v0

    invoke-virtual {v1, v0}, Lpmsj/work/main/i;->b([B)V

    return-void
.end method

.method public static a(IBB)V
    .locals 2

    new-instance v0, La/c/r;

    invoke-direct {v0, p0}, La/c/r;-><init>(I)V

    invoke-virtual {v0, p1}, La/c/r;->b(I)V

    invoke-virtual {v0, p2}, La/c/r;->b(I)V

    sget-object v1, Lpmsj/work/main/e;->a:Lpmsj/work/main/i;

    invoke-virtual {v0}, La/c/r;->a()[B

    move-result-object v0

    invoke-virtual {v1, v0}, Lpmsj/work/main/i;->b([B)V

    return-void
.end method

.method public static a(IBBB)V
    .locals 2

    new-instance v0, La/c/r;

    invoke-direct {v0, p0}, La/c/r;-><init>(I)V

    invoke-virtual {v0, p1}, La/c/r;->b(I)V

    invoke-virtual {v0, p2}, La/c/r;->b(I)V

    invoke-virtual {v0, p3}, La/c/r;->b(I)V

    sget-object v1, Lpmsj/work/main/e;->a:Lpmsj/work/main/i;

    invoke-virtual {v0}, La/c/r;->a()[B

    move-result-object v0

    invoke-virtual {v1, v0}, Lpmsj/work/main/i;->b([B)V

    return-void
.end method

.method public static a(IBBBB)V
    .locals 2

    new-instance v0, La/c/r;

    invoke-direct {v0, p0}, La/c/r;-><init>(I)V

    invoke-virtual {v0, p1}, La/c/r;->b(I)V

    invoke-virtual {v0, p2}, La/c/r;->b(I)V

    invoke-virtual {v0, p3}, La/c/r;->b(I)V

    invoke-virtual {v0, p4}, La/c/r;->b(I)V

    sget-object v1, Lpmsj/work/main/e;->a:Lpmsj/work/main/i;

    invoke-virtual {v0}, La/c/r;->a()[B

    move-result-object v0

    invoke-virtual {v1, v0}, Lpmsj/work/main/i;->b([B)V

    return-void
.end method

.method public static a(IBBI)V
    .locals 2

    new-instance v0, La/c/r;

    invoke-direct {v0}, La/c/r;-><init>()V

    const/16 v1, 0x479

    invoke-virtual {v0, v1}, La/c/r;->a(I)V

    const/4 v1, 0x0

    invoke-virtual {v0, v1}, La/c/r;->b(I)V

    invoke-virtual {v0, p0}, La/c/r;->d(I)V

    invoke-virtual {v0, p1}, La/c/r;->b(I)V

    invoke-virtual {v0, p2}, La/c/r;->b(I)V

    invoke-virtual {v0, p3}, La/c/r;->d(I)V

    sget-object v1, Lpmsj/work/main/e;->a:Lpmsj/work/main/i;

    invoke-virtual {v0}, La/c/r;->a()[B

    move-result-object v0

    invoke-virtual {v1, v0}, Lpmsj/work/main/i;->b([B)V

    return-void
.end method

.method public static a(IBI)V
    .locals 2

    new-instance v0, La/c/r;

    invoke-direct {v0, p0}, La/c/r;-><init>(I)V

    invoke-virtual {v0, p1}, La/c/r;->b(I)V

    invoke-virtual {v0, p2}, La/c/r;->d(I)V

    sget-object v1, Lpmsj/work/main/e;->a:Lpmsj/work/main/i;

    invoke-virtual {v0}, La/c/r;->a()[B

    move-result-object v0

    invoke-virtual {v1, v0}, Lpmsj/work/main/i;->b([B)V

    return-void
.end method

.method public static a(IBIB)V
    .locals 2

    new-instance v0, La/c/r;

    invoke-direct {v0}, La/c/r;-><init>()V

    invoke-virtual {v0, p0}, La/c/r;->a(I)V

    invoke-virtual {v0, p1}, La/c/r;->b(I)V

    invoke-virtual {v0, p2}, La/c/r;->d(I)V

    invoke-virtual {v0, p3}, La/c/r;->b(I)V

    sget-object v1, Lpmsj/work/main/e;->a:Lpmsj/work/main/i;

    invoke-virtual {v0}, La/c/r;->a()[B

    move-result-object v0

    invoke-virtual {v1, v0}, Lpmsj/work/main/i;->b([B)V

    return-void
.end method

.method public static a(IBIBB)V
    .locals 2

    new-instance v0, La/c/r;

    invoke-direct {v0}, La/c/r;-><init>()V

    invoke-virtual {v0, p0}, La/c/r;->a(I)V

    invoke-virtual {v0, p1}, La/c/r;->b(I)V

    invoke-virtual {v0, p2}, La/c/r;->d(I)V

    invoke-virtual {v0, p3}, La/c/r;->b(I)V

    invoke-virtual {v0, p4}, La/c/r;->b(I)V

    sget-object v1, Lpmsj/work/main/e;->a:Lpmsj/work/main/i;

    invoke-virtual {v0}, La/c/r;->a()[B

    move-result-object v0

    invoke-virtual {v1, v0}, Lpmsj/work/main/i;->b([B)V

    return-void
.end method

.method public static a(IBIBIB)V
    .locals 2

    new-instance v0, La/c/r;

    invoke-direct {v0}, La/c/r;-><init>()V

    invoke-virtual {v0, p0}, La/c/r;->a(I)V

    invoke-virtual {v0, p1}, La/c/r;->b(I)V

    invoke-virtual {v0, p2}, La/c/r;->d(I)V

    invoke-virtual {v0, p3}, La/c/r;->b(I)V

    invoke-virtual {v0, p4}, La/c/r;->d(I)V

    invoke-virtual {v0, p5}, La/c/r;->b(I)V

    sget-object v1, Lpmsj/work/main/e;->a:Lpmsj/work/main/i;

    invoke-virtual {v0}, La/c/r;->a()[B

    move-result-object v0

    invoke-virtual {v1, v0}, Lpmsj/work/main/i;->b([B)V

    return-void
.end method

.method public static a(IBII)V
    .locals 2

    new-instance v0, La/c/r;

    invoke-direct {v0}, La/c/r;-><init>()V

    invoke-virtual {v0, p0}, La/c/r;->a(I)V

    invoke-virtual {v0, p1}, La/c/r;->b(I)V

    invoke-virtual {v0, p2}, La/c/r;->d(I)V

    invoke-virtual {v0, p3}, La/c/r;->d(I)V

    sget-object v1, Lpmsj/work/main/e;->a:Lpmsj/work/main/i;

    invoke-virtual {v0}, La/c/r;->a()[B

    move-result-object v0

    invoke-virtual {v1, v0}, Lpmsj/work/main/i;->b([B)V

    return-void
.end method

.method public static a(IBIIB)V
    .locals 2

    new-instance v0, La/c/r;

    invoke-direct {v0}, La/c/r;-><init>()V

    invoke-virtual {v0, p0}, La/c/r;->a(I)V

    invoke-virtual {v0, p1}, La/c/r;->b(I)V

    invoke-virtual {v0, p2}, La/c/r;->d(I)V

    invoke-virtual {v0, p3}, La/c/r;->d(I)V

    invoke-virtual {v0, p4}, La/c/r;->b(I)V

    sget-object v1, Lpmsj/work/main/e;->a:Lpmsj/work/main/i;

    invoke-virtual {v0}, La/c/r;->a()[B

    move-result-object v0

    invoke-virtual {v1, v0}, Lpmsj/work/main/i;->b([B)V

    return-void
.end method

.method public static a(IBIIBB)V
    .locals 2

    new-instance v0, La/c/r;

    invoke-direct {v0}, La/c/r;-><init>()V

    invoke-virtual {v0, p0}, La/c/r;->a(I)V

    invoke-virtual {v0, p1}, La/c/r;->b(I)V

    invoke-virtual {v0, p2}, La/c/r;->d(I)V

    invoke-virtual {v0, p3}, La/c/r;->d(I)V

    invoke-virtual {v0, p4}, La/c/r;->b(I)V

    invoke-virtual {v0, p5}, La/c/r;->b(I)V

    sget-object v1, Lpmsj/work/main/e;->a:Lpmsj/work/main/i;

    invoke-virtual {v0}, La/c/r;->a()[B

    move-result-object v0

    invoke-virtual {v1, v0}, Lpmsj/work/main/i;->b([B)V

    return-void
.end method

.method public static a(IBIII)V
    .locals 2

    new-instance v0, La/c/r;

    invoke-direct {v0}, La/c/r;-><init>()V

    invoke-virtual {v0, p0}, La/c/r;->a(I)V

    invoke-virtual {v0, p1}, La/c/r;->b(I)V

    invoke-virtual {v0, p2}, La/c/r;->d(I)V

    invoke-virtual {v0, p3}, La/c/r;->d(I)V

    invoke-virtual {v0, p4}, La/c/r;->d(I)V

    sget-object v1, Lpmsj/work/main/e;->a:Lpmsj/work/main/i;

    invoke-virtual {v0}, La/c/r;->a()[B

    move-result-object v0

    invoke-virtual {v1, v0}, Lpmsj/work/main/i;->b([B)V

    return-void
.end method

.method public static a(IBIIIII)V
    .locals 2

    new-instance v0, La/c/r;

    invoke-direct {v0}, La/c/r;-><init>()V

    invoke-virtual {v0, p0}, La/c/r;->a(I)V

    invoke-virtual {v0, p1}, La/c/r;->b(I)V

    invoke-virtual {v0, p2}, La/c/r;->d(I)V

    invoke-virtual {v0, p3}, La/c/r;->d(I)V

    invoke-virtual {v0, p4}, La/c/r;->d(I)V

    invoke-virtual {v0, p5}, La/c/r;->d(I)V

    invoke-virtual {v0, p6}, La/c/r;->d(I)V

    sget-object v1, Lpmsj/work/main/e;->a:Lpmsj/work/main/i;

    invoke-virtual {v0}, La/c/r;->a()[B

    move-result-object v0

    invoke-virtual {v1, v0}, Lpmsj/work/main/i;->b([B)V

    return-void
.end method

.method public static a(IB[I)V
    .locals 4

    new-instance v0, La/c/r;

    invoke-direct {v0}, La/c/r;-><init>()V

    invoke-virtual {v0, p0}, La/c/r;->a(I)V

    invoke-virtual {v0, p1}, La/c/r;->b(I)V

    array-length v1, p2

    int-to-byte v1, v1

    invoke-virtual {v0, v1}, La/c/r;->b(I)V

    const/4 v2, 0x0

    :goto_0
    if-ge v2, v1, :cond_0

    aget v3, p2, v2

    invoke-virtual {v0, v3}, La/c/r;->d(I)V

    add-int/lit8 v2, v2, 0x1

    int-to-byte v2, v2

    goto :goto_0

    :cond_0
    sget-object v1, Lpmsj/work/main/e;->a:Lpmsj/work/main/i;

    invoke-virtual {v0}, La/c/r;->a()[B

    move-result-object v0

    invoke-virtual {v1, v0}, Lpmsj/work/main/i;->b([B)V

    return-void
.end method

.method public static a(ILa/c/i;La/c/i;)V
    .locals 2

    new-instance v0, La/c/r;

    invoke-direct {v0}, La/c/r;-><init>()V

    invoke-virtual {v0, p0}, La/c/r;->a(I)V

    invoke-virtual {v0, p1}, La/c/r;->a(La/c/i;)V

    invoke-virtual {v0, p2}, La/c/r;->a(La/c/i;)V

    sget-object v1, Lpmsj/work/main/e;->a:Lpmsj/work/main/i;

    invoke-virtual {v0}, La/c/r;->a()[B

    move-result-object v0

    invoke-virtual {v1, v0}, Lpmsj/work/main/i;->b([B)V

    return-void
.end method

.method public static a(ILa/c/i;La/c/i;La/c/i;)V
    .locals 2

    new-instance v0, La/c/r;

    invoke-direct {v0}, La/c/r;-><init>()V

    invoke-virtual {v0, p0}, La/c/r;->a(I)V

    invoke-virtual {v0, p1}, La/c/r;->a(La/c/i;)V

    invoke-virtual {v0, p2}, La/c/r;->a(La/c/i;)V

    invoke-virtual {v0, p3}, La/c/r;->a(La/c/i;)V

    sget-object v1, Lpmsj/work/main/e;->a:Lpmsj/work/main/i;

    invoke-virtual {v0}, La/c/r;->a()[B

    move-result-object v0

    invoke-virtual {v1, v0}, Lpmsj/work/main/i;->b([B)V

    return-void
.end method

.method public static a(ILa/c/i;La/c/i;La/c/i;La/c/i;)V
    .locals 2

    new-instance v0, La/c/r;

    invoke-direct {v0}, La/c/r;-><init>()V

    invoke-virtual {v0, p0}, La/c/r;->a(I)V

    invoke-virtual {v0, p1}, La/c/r;->a(La/c/i;)V

    invoke-virtual {v0, p2}, La/c/r;->a(La/c/i;)V

    invoke-virtual {v0, p3}, La/c/r;->a(La/c/i;)V

    invoke-virtual {v0, p4}, La/c/r;->a(La/c/i;)V

    sget-object v1, Lpmsj/work/main/e;->a:Lpmsj/work/main/i;

    invoke-virtual {v0}, La/c/r;->a()[B

    move-result-object v0

    invoke-virtual {v1, v0}, Lpmsj/work/main/i;->b([B)V

    return-void
.end method

.method public static a(ILa/c/i;La/c/i;La/c/i;La/c/i;La/c/i;)V
    .locals 2

    new-instance v0, La/c/r;

    invoke-direct {v0}, La/c/r;-><init>()V

    invoke-virtual {v0, p0}, La/c/r;->a(I)V

    invoke-virtual {v0, p1}, La/c/r;->a(La/c/i;)V

    invoke-virtual {v0, p2}, La/c/r;->a(La/c/i;)V

    invoke-virtual {v0, p3}, La/c/r;->a(La/c/i;)V

    invoke-virtual {v0, p4}, La/c/r;->a(La/c/i;)V

    invoke-virtual {v0, p5}, La/c/r;->a(La/c/i;)V

    sget-object v1, Lpmsj/work/main/e;->a:Lpmsj/work/main/i;

    invoke-virtual {v0}, La/c/r;->a()[B

    move-result-object v0

    invoke-virtual {v1, v0}, Lpmsj/work/main/i;->b([B)V

    return-void
.end method

.method public static a(ILa/c/i;La/c/i;La/c/i;La/c/i;La/c/i;La/c/i;)V
    .locals 2

    new-instance v0, La/c/r;

    invoke-direct {v0}, La/c/r;-><init>()V

    invoke-virtual {v0, p0}, La/c/r;->a(I)V

    invoke-virtual {v0, p1}, La/c/r;->a(La/c/i;)V

    invoke-virtual {v0, p2}, La/c/r;->a(La/c/i;)V

    invoke-virtual {v0, p3}, La/c/r;->a(La/c/i;)V

    invoke-virtual {v0, p4}, La/c/r;->a(La/c/i;)V

    invoke-virtual {v0, p5}, La/c/r;->a(La/c/i;)V

    invoke-virtual {v0, p6}, La/c/r;->a(La/c/i;)V

    sget-object v1, Lpmsj/work/main/e;->a:Lpmsj/work/main/i;

    invoke-virtual {v0}, La/c/r;->a()[B

    move-result-object v0

    invoke-virtual {v1, v0}, Lpmsj/work/main/i;->b([B)V

    return-void
.end method

.method public static a(ILa/c/i;La/c/i;La/c/i;La/c/i;La/c/i;La/c/i;La/c/i;)V
    .locals 2

    new-instance v0, La/c/r;

    invoke-direct {v0}, La/c/r;-><init>()V

    invoke-virtual {v0, p0}, La/c/r;->a(I)V

    invoke-virtual {v0, p1}, La/c/r;->a(La/c/i;)V

    invoke-virtual {v0, p2}, La/c/r;->a(La/c/i;)V

    invoke-virtual {v0, p3}, La/c/r;->a(La/c/i;)V

    invoke-virtual {v0, p4}, La/c/r;->a(La/c/i;)V

    invoke-virtual {v0, p5}, La/c/r;->a(La/c/i;)V

    invoke-virtual {v0, p6}, La/c/r;->a(La/c/i;)V

    invoke-virtual {v0, p7}, La/c/r;->a(La/c/i;)V

    sget-object v1, Lpmsj/work/main/e;->a:Lpmsj/work/main/i;

    invoke-virtual {v0}, La/c/r;->a()[B

    move-result-object v0

    invoke-virtual {v1, v0}, Lpmsj/work/main/i;->b([B)V

    return-void
.end method

.method public static a(ILa/c/i;La/c/i;La/c/i;La/c/i;La/c/i;La/c/i;La/c/i;La/c/i;)V
    .locals 2

    new-instance v0, La/c/r;

    invoke-direct {v0}, La/c/r;-><init>()V

    invoke-virtual {v0, p0}, La/c/r;->a(I)V

    invoke-virtual {v0, p1}, La/c/r;->a(La/c/i;)V

    invoke-virtual {v0, p2}, La/c/r;->a(La/c/i;)V

    invoke-virtual {v0, p3}, La/c/r;->a(La/c/i;)V

    invoke-virtual {v0, p4}, La/c/r;->a(La/c/i;)V

    invoke-virtual {v0, p5}, La/c/r;->a(La/c/i;)V

    invoke-virtual {v0, p6}, La/c/r;->a(La/c/i;)V

    invoke-virtual {v0, p7}, La/c/r;->a(La/c/i;)V

    invoke-virtual {v0, p8}, La/c/r;->a(La/c/i;)V

    sget-object v1, Lpmsj/work/main/e;->a:Lpmsj/work/main/i;

    invoke-virtual {v0}, La/c/r;->a()[B

    move-result-object v0

    invoke-virtual {v1, v0}, Lpmsj/work/main/i;->b([B)V

    return-void
.end method

.method public static a(IS)V
    .locals 2

    new-instance v0, La/c/r;

    invoke-direct {v0}, La/c/r;-><init>()V

    invoke-virtual {v0, p0}, La/c/r;->a(I)V

    invoke-virtual {v0, p1}, La/c/r;->c(I)V

    sget-object v1, Lpmsj/work/main/e;->a:Lpmsj/work/main/i;

    invoke-virtual {v0}, La/c/r;->a()[B

    move-result-object v0

    invoke-virtual {v1, v0}, Lpmsj/work/main/i;->b([B)V

    return-void
.end method

.method public static a(ISI)V
    .locals 4

    const-string v3, ","

    new-instance v0, La/c/r;

    invoke-direct {v0}, La/c/r;-><init>()V

    invoke-virtual {v0, p0}, La/c/r;->a(I)V

    invoke-virtual {v0, p1}, La/c/r;->c(I)V

    invoke-virtual {v0, p2}, La/c/r;->d(I)V

    sget-object v1, Lpmsj/work/main/e;->a:Lpmsj/work/main/i;

    invoke-virtual {v0}, La/c/r;->a()[B

    move-result-object v0

    invoke-virtual {v1, v0}, Lpmsj/work/main/i;->b([B)V

    sget-object v0, Ljava/lang/System;->out:Ljava/io/PrintStream;

    new-instance v1, Ljava/lang/StringBuilder;

    invoke-direct {v1}, Ljava/lang/StringBuilder;-><init>()V

    const-string v2, "====="

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    invoke-virtual {v1, p0}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    move-result-object v1

    const-string v2, ","

    invoke-virtual {v1, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    invoke-virtual {v1, p1}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    move-result-object v1

    const-string v2, ","

    invoke-virtual {v1, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    invoke-virtual {v1, p2}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    move-result-object v1

    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v1

    invoke-virtual {v0, v1}, Ljava/io/PrintStream;->println(Ljava/lang/String;)V

    return-void
.end method

.method public static a(ISII)V
    .locals 2

    new-instance v0, La/c/r;

    invoke-direct {v0, p0}, La/c/r;-><init>(I)V

    invoke-virtual {v0, p1}, La/c/r;->c(I)V

    invoke-virtual {v0, p2}, La/c/r;->d(I)V

    invoke-virtual {v0, p3}, La/c/r;->d(I)V

    sget-object v1, Lpmsj/work/main/e;->a:Lpmsj/work/main/i;

    invoke-virtual {v0}, La/c/r;->a()[B

    move-result-object v0

    invoke-virtual {v1, v0}, Lpmsj/work/main/i;->b([B)V

    return-void
.end method

.method public static a(La/c/i;)V
    .locals 2

    new-instance v0, La/c/r;

    invoke-direct {v0}, La/c/r;-><init>()V

    const/16 v1, 0x7cf

    invoke-virtual {v0, v1}, La/c/r;->a(I)V

    invoke-virtual {v0, p0}, La/c/r;->a(La/c/i;)V

    sget-object v1, Lpmsj/work/main/e;->a:Lpmsj/work/main/i;

    invoke-virtual {v0}, La/c/r;->a()[B

    move-result-object v0

    invoke-virtual {v1, v0}, Lpmsj/work/main/i;->b([B)V

    return-void
.end method

.method public static a(La/c/i;La/c/i;La/c/i;[La/c/i;)V
    .locals 3

    new-instance v0, La/c/r;

    invoke-direct {v0}, La/c/r;-><init>()V

    const/16 v1, 0x3f1

    invoke-virtual {v0, v1}, La/c/r;->a(I)V

    invoke-virtual {v0, p0}, La/c/r;->a(La/c/i;)V

    invoke-virtual {v0, p1}, La/c/r;->a(La/c/i;)V

    invoke-virtual {v0, p2}, La/c/r;->a(La/c/i;)V

    const/4 v1, 0x0

    :goto_0
    array-length v2, p3

    if-ge v1, v2, :cond_0

    aget-object v2, p3, v1

    invoke-virtual {v0, v2}, La/c/r;->a(La/c/i;)V

    add-int/lit8 v1, v1, 0x1

    goto :goto_0

    :cond_0
    sget-object v1, Lpmsj/work/main/e;->a:Lpmsj/work/main/i;

    invoke-virtual {v0}, La/c/r;->a()[B

    move-result-object v0

    invoke-virtual {v1, v0}, Lpmsj/work/main/i;->b([B)V

    return-void
.end method

.method public static a(La/c/i;La/c/i;[I)V
    .locals 4

    new-instance v0, La/c/r;

    invoke-direct {v0}, La/c/r;-><init>()V

    const/16 v1, 0x5dc

    invoke-virtual {v0, v1}, La/c/r;->a(I)V

    invoke-virtual {v0, p0}, La/c/r;->a(La/c/i;)V

    invoke-virtual {v0, p1}, La/c/r;->a(La/c/i;)V

    const/4 v1, 0x0

    :goto_0
    array-length v2, p2

    if-ge v1, v2, :cond_0

    new-instance v2, La/c/m;

    aget v3, p2, v1

    invoke-direct {v2, v3}, La/c/m;-><init>(I)V

    invoke-virtual {v0, v2}, La/c/r;->a(La/c/i;)V

    add-int/lit8 v1, v1, 0x1

    int-to-byte v1, v1

    goto :goto_0

    :cond_0
    sget-object v1, Lpmsj/work/main/e;->a:Lpmsj/work/main/i;

    invoke-virtual {v0}, La/c/r;->a()[B

    move-result-object v0

    invoke-virtual {v1, v0}, Lpmsj/work/main/i;->b([B)V

    return-void
.end method

.method public static b(II)V
    .locals 2

    new-instance v0, La/c/r;

    invoke-direct {v0}, La/c/r;-><init>()V

    invoke-virtual {v0, p0}, La/c/r;->a(I)V

    invoke-virtual {v0, p1}, La/c/r;->d(I)V

    sget-object v1, Lpmsj/work/main/e;->a:Lpmsj/work/main/i;

    invoke-virtual {v0}, La/c/r;->a()[B

    move-result-object v0

    invoke-virtual {v1, v0}, Lpmsj/work/main/i;->b([B)V

    return-void
.end method


# virtual methods
.method public final a(I)B
    .locals 1

    iget-object v0, p0, Lpmsj/work/main/w;->b:Ljava/util/Vector;

    invoke-virtual {v0, p1}, Ljava/util/Vector;->elementAt(I)Ljava/lang/Object;

    move-result-object p0

    check-cast p0, La/c/h;

    iget-byte v0, p0, La/c/h;->a:B

    return v0
.end method

.method public final a(II)La/c/a;
    .locals 5

    new-instance v1, La/c/a;

    invoke-direct {v1, p1}, La/c/a;-><init>(I)V

    iget-object v2, v1, La/c/a;->a:[La/c/i;

    const/4 v0, 0x0

    move v3, v0

    :goto_0
    if-ge v3, p1, :cond_0

    iget-object v0, p0, Lpmsj/work/main/w;->b:Ljava/util/Vector;

    add-int v4, v3, p2

    invoke-virtual {v0, v4}, Ljava/util/Vector;->elementAt(I)Ljava/lang/Object;

    move-result-object v0

    check-cast v0, La/c/i;

    aput-object v0, v2, v3

    add-int/lit8 v0, v3, 0x1

    move v3, v0

    goto :goto_0

    :cond_0
    return-object v1
.end method

.method public final b(I)S
    .locals 1

    iget-object v0, p0, Lpmsj/work/main/w;->b:Ljava/util/Vector;

    invoke-virtual {v0, p1}, Ljava/util/Vector;->elementAt(I)Ljava/lang/Object;

    move-result-object p0

    check-cast p0, La/c/o;

    iget-short v0, p0, La/c/o;->a:S

    return v0
.end method

.method public final c(I)I
    .locals 1

    iget-object v0, p0, Lpmsj/work/main/w;->b:Ljava/util/Vector;

    invoke-virtual {v0, p1}, Ljava/util/Vector;->elementAt(I)Ljava/lang/Object;

    move-result-object p0

    check-cast p0, La/c/i;

    invoke-virtual {p0}, La/c/i;->b()I

    move-result v0

    return v0
.end method

.method public final d(I)I
    .locals 1

    iget-object v0, p0, Lpmsj/work/main/w;->b:Ljava/util/Vector;

    invoke-virtual {v0, p1}, Ljava/util/Vector;->elementAt(I)Ljava/lang/Object;

    move-result-object p0

    check-cast p0, La/c/i;

    invoke-virtual {p0}, La/c/i;->b()I

    move-result v0

    return v0
.end method

.method public final e(I)Ljava/lang/String;
    .locals 1

    iget-object v0, p0, Lpmsj/work/main/w;->b:Ljava/util/Vector;

    invoke-virtual {v0, p1}, Ljava/util/Vector;->elementAt(I)Ljava/lang/Object;

    move-result-object p0

    check-cast p0, La/c/p;

    invoke-virtual {p0}, La/c/p;->e()Ljava/lang/String;

    move-result-object v0

    return-object v0
.end method

.method public final f(I)[B
    .locals 1

    iget-object v0, p0, Lpmsj/work/main/w;->b:Ljava/util/Vector;

    invoke-virtual {v0, p1}, Ljava/util/Vector;->elementAt(I)Ljava/lang/Object;

    move-result-object p0

    check-cast p0, [B

    return-object p0
.end method

.method public final g(I)La/c/i;
    .locals 1

    iget-object v0, p0, Lpmsj/work/main/w;->b:Ljava/util/Vector;

    invoke-virtual {v0, p1}, Ljava/util/Vector;->elementAt(I)Ljava/lang/Object;

    move-result-object p0

    check-cast p0, La/c/i;

    return-object p0
.end method
