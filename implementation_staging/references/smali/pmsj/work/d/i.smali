.class public final Lpmsj/work/d/i;
.super Ljava/lang/Object;


# instance fields
.field private a:S

.field private b:B

.field private c:S


# direct methods
.method public constructor <init>(I)V
    .locals 1

    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    int-to-byte v0, p1

    iput-byte v0, p0, Lpmsj/work/d/i;->b:B

    return-void
.end method

.method private e(I)Z
    .locals 2

    iget-short v0, p0, Lpmsj/work/d/i;->c:S

    add-int/2addr v0, p1

    iget-short v1, p0, Lpmsj/work/d/i;->a:S

    if-ge v0, v1, :cond_0

    const/4 v0, 0x1

    :goto_0
    return v0

    :cond_0
    const/4 v0, 0x0

    goto :goto_0
.end method


# virtual methods
.method public final a()I
    .locals 1

    iget-short v0, p0, Lpmsj/work/d/i;->a:S

    return v0
.end method

.method public final a(I)V
    .locals 1

    int-to-short v0, p1

    iput-short v0, p0, Lpmsj/work/d/i;->a:S

    return-void
.end method

.method public final b(I)I
    .locals 3

    iget-short v0, p0, Lpmsj/work/d/i;->c:S

    iget-short v1, p0, Lpmsj/work/d/i;->a:S

    iget-byte v2, p0, Lpmsj/work/d/i;->b:B

    sub-int/2addr v1, v2

    add-int/lit8 v1, v1, 0x1

    iget-short v2, p0, Lpmsj/work/d/i;->c:S

    add-int/2addr v2, p1

    invoke-static {v1, v2}, Ljava/lang/Math;->min(II)I

    move-result v1

    int-to-short v1, v1

    iput-short v1, p0, Lpmsj/work/d/i;->c:S

    iget-short v1, p0, Lpmsj/work/d/i;->c:S

    sub-int v0, v1, v0

    return v0
.end method

.method public final b()V
    .locals 1

    const/4 v0, 0x0

    iput-short v0, p0, Lpmsj/work/d/i;->c:S

    iput-short v0, p0, Lpmsj/work/d/i;->a:S

    return-void
.end method

.method public final c()I
    .locals 3

    iget-byte v0, p0, Lpmsj/work/d/i;->b:B

    if-nez v0, :cond_1

    const/4 v0, 0x0

    :cond_0
    :goto_0
    return v0

    :cond_1
    iget-short v0, p0, Lpmsj/work/d/i;->c:S

    iget-byte v1, p0, Lpmsj/work/d/i;->b:B

    div-int/2addr v0, v1

    iget-short v1, p0, Lpmsj/work/d/i;->c:S

    iget-byte v2, p0, Lpmsj/work/d/i;->b:B

    rem-int/2addr v1, v2

    if-lez v1, :cond_0

    add-int/lit8 v0, v0, 0x1

    goto :goto_0
.end method

.method public final c(I)I
    .locals 3

    iget-short v0, p0, Lpmsj/work/d/i;->c:S

    const/4 v1, 0x0

    iget-short v2, p0, Lpmsj/work/d/i;->c:S

    sub-int/2addr v2, p1

    invoke-static {v1, v2}, Ljava/lang/Math;->max(II)I

    move-result v1

    int-to-short v1, v1

    iput-short v1, p0, Lpmsj/work/d/i;->c:S

    iget-short v1, p0, Lpmsj/work/d/i;->c:S

    sub-int/2addr v0, v1

    return v0
.end method

.method public final d()I
    .locals 1

    iget-byte v0, p0, Lpmsj/work/d/i;->b:B

    return v0
.end method

.method public final d(I)Z
    .locals 3

    const/4 v2, 0x0

    iget-short v0, p0, Lpmsj/work/d/i;->a:S

    if-nez v0, :cond_0

    move v0, v2

    :goto_0
    return v0

    :cond_0
    iget-short v0, p0, Lpmsj/work/d/i;->a:S

    if-le p1, v0, :cond_1

    move v0, v2

    goto :goto_0

    :cond_1
    iget-short v0, p0, Lpmsj/work/d/i;->c:S

    iget-byte v1, p0, Lpmsj/work/d/i;->b:B

    add-int/2addr v0, v1

    if-le v0, p1, :cond_2

    const/4 v0, 0x1

    goto :goto_0

    :cond_2
    move v0, v2

    goto :goto_0
.end method

.method public final e()I
    .locals 1

    iget-short v0, p0, Lpmsj/work/d/i;->c:S

    return v0
.end method

.method public final f()I
    .locals 2

    iget-short v0, p0, Lpmsj/work/d/i;->c:S

    iget-byte v1, p0, Lpmsj/work/d/i;->b:B

    add-int/2addr v0, v1

    return v0
.end method

.method public final g()Z
    .locals 2

    iget-byte v0, p0, Lpmsj/work/d/i;->b:B

    const/4 v1, 0x2

    sub-int/2addr v0, v1

    invoke-direct {p0, v0}, Lpmsj/work/d/i;->e(I)Z

    move-result v0

    return v0
.end method

.method public final h()Z
    .locals 3

    const/4 v2, 0x1

    iget-short v0, p0, Lpmsj/work/d/i;->a:S

    iget-short v1, p0, Lpmsj/work/d/i;->c:S

    if-le v0, v1, :cond_0

    iget-byte v0, p0, Lpmsj/work/d/i;->b:B

    invoke-direct {p0, v0}, Lpmsj/work/d/i;->e(I)Z

    move-result v0

    if-nez v0, :cond_1

    :cond_0
    const/4 v0, 0x0

    :goto_0
    return v0

    :cond_1
    iget-short v0, p0, Lpmsj/work/d/i;->c:S

    add-int/lit8 v0, v0, 0x2

    int-to-short v0, v0

    iput-short v0, p0, Lpmsj/work/d/i;->c:S

    iget-short v0, p0, Lpmsj/work/d/i;->c:S

    iget-short v1, p0, Lpmsj/work/d/i;->a:S

    if-lt v0, v1, :cond_2

    iget-short v0, p0, Lpmsj/work/d/i;->a:S

    sub-int/2addr v0, v2

    int-to-short v0, v0

    iput-short v0, p0, Lpmsj/work/d/i;->c:S

    :cond_2
    move v0, v2

    goto :goto_0
.end method

.method public final i()Z
    .locals 1

    iget-short v0, p0, Lpmsj/work/d/i;->c:S

    if-lez v0, :cond_0

    const/4 v0, 0x1

    :goto_0
    return v0

    :cond_0
    const/4 v0, 0x0

    goto :goto_0
.end method

.method public final j()Z
    .locals 3

    const/4 v2, 0x0

    invoke-virtual {p0}, Lpmsj/work/d/i;->i()Z

    move-result v0

    if-nez v0, :cond_0

    move v0, v2

    :goto_0
    return v0

    :cond_0
    iget-short v0, p0, Lpmsj/work/d/i;->c:S

    const/4 v1, 0x2

    sub-int/2addr v0, v1

    int-to-short v0, v0

    iput-short v0, p0, Lpmsj/work/d/i;->c:S

    iget-short v0, p0, Lpmsj/work/d/i;->c:S

    invoke-static {v0, v2}, Ljava/lang/Math;->max(II)I

    move-result v0

    int-to-short v0, v0

    iput-short v0, p0, Lpmsj/work/d/i;->c:S

    const/4 v0, 0x1

    goto :goto_0
.end method

.method public final k()Z
    .locals 2

    const/4 v1, 0x1

    iget-short v0, p0, Lpmsj/work/d/i;->c:S

    if-nez v0, :cond_0

    const/4 v0, 0x0

    :goto_0
    return v0

    :cond_0
    iget-short v0, p0, Lpmsj/work/d/i;->c:S

    sub-int/2addr v0, v1

    int-to-short v0, v0

    iput-short v0, p0, Lpmsj/work/d/i;->c:S

    move v0, v1

    goto :goto_0
.end method

.method public final l()Z
    .locals 3

    iget-short v0, p0, Lpmsj/work/d/i;->c:S

    iget-short v1, p0, Lpmsj/work/d/i;->a:S

    iget-byte v2, p0, Lpmsj/work/d/i;->b:B

    sub-int/2addr v1, v2

    if-le v0, v1, :cond_0

    const/4 v0, 0x0

    :goto_0
    return v0

    :cond_0
    iget-short v0, p0, Lpmsj/work/d/i;->c:S

    add-int/lit8 v0, v0, 0x1

    int-to-short v0, v0

    iput-short v0, p0, Lpmsj/work/d/i;->c:S

    const/4 v0, 0x1

    goto :goto_0
.end method
