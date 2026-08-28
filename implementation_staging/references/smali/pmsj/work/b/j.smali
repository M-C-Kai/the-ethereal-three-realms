.class public Lpmsj/work/b/j;
.super Ljava/lang/Object;


# instance fields
.field public e:I

.field public f:I

.field public g:S

.field public h:S

.field public i:I

.field public j:S

.field public k:B

.field public l:S

.field public m:I

.field public n:B

.field public o:Ljava/lang/String;

.field public p:I

.field public q:S

.field public r:J

.field public s:S

.field public t:S

.field public u:I

.field public v:I

.field protected w:I


# direct methods
.method public constructor <init>(II)V
    .locals 1

    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    const/4 v0, -0x1

    iput v0, p0, Lpmsj/work/b/j;->p:I

    sget v0, La/c/x;->a:I

    iput v0, p0, Lpmsj/work/b/j;->w:I

    iput p1, p0, Lpmsj/work/b/j;->e:I

    iput p2, p0, Lpmsj/work/b/j;->f:I

    return-void
.end method

.method public static b(BI)Z
    .locals 1

    invoke-static {p1}, Lpmsj/work/b/j;->f(I)B

    move-result v0

    if-ne p0, v0, :cond_0

    const/4 v0, 0x1

    :goto_0
    return v0

    :cond_0
    const/4 v0, 0x0

    goto :goto_0
.end method

.method public static f(I)B
    .locals 1

    const v0, 0x989680

    div-int v0, p0, v0

    rem-int/lit8 v0, v0, 0x64

    int-to-byte v0, v0

    return v0
.end method

.method public static g(I)Z
    .locals 2

    invoke-static {p0}, Lpmsj/work/b/j;->f(I)B

    move-result v0

    if-lez v0, :cond_0

    const/16 v1, 0x15

    if-gt v0, v1, :cond_0

    const/4 v0, 0x1

    :goto_0
    return v0

    :cond_0
    const/4 v0, 0x0

    goto :goto_0
.end method

.method public static h(I)Z
    .locals 2

    invoke-static {p0}, Lpmsj/work/b/j;->f(I)B

    move-result v0

    const/16 v1, 0x11

    if-ne v0, v1, :cond_0

    const/4 v0, 0x1

    :goto_0
    return v0

    :cond_0
    const/4 v0, 0x0

    goto :goto_0
.end method

.method public static i(I)Z
    .locals 2

    const v0, 0xf4240

    div-int v0, p0, v0

    const/16 v1, 0x149

    if-ne v0, v1, :cond_0

    const/4 v0, 0x1

    :goto_0
    return v0

    :cond_0
    const/4 v0, 0x0

    goto :goto_0
.end method

.method public static j(I)I
    .locals 1

    invoke-static {p0}, Lpmsj/work/b/j;->g(I)Z

    move-result v0

    if-eqz v0, :cond_0

    rem-int/lit8 v0, p0, 0xa

    :goto_0
    return v0

    :cond_0
    const/4 v0, 0x0

    goto :goto_0
.end method


# virtual methods
.method public a()Ljava/lang/String;
    .locals 1

    const-string v0, ""

    return-object v0
.end method

.method public b()Z
    .locals 1

    const/4 v0, 0x0

    return v0
.end method

.method public final c(I)V
    .locals 0

    iput p1, p0, Lpmsj/work/b/j;->w:I

    return-void
.end method

.method public c()Z
    .locals 1

    const/4 v0, 0x0

    return v0
.end method

.method public d()Ljava/lang/String;
    .locals 1

    iget-object v0, p0, Lpmsj/work/b/j;->o:Ljava/lang/String;

    return-object v0
.end method

.method public final d(I)Z
    .locals 1

    iget-short v0, p0, Lpmsj/work/b/j;->l:S

    and-int/2addr v0, p1

    if-eqz v0, :cond_0

    const/4 v0, 0x1

    :goto_0
    return v0

    :cond_0
    const/4 v0, 0x0

    goto :goto_0
.end method

.method public final e(I)Z
    .locals 1

    iget v0, p0, Lpmsj/work/b/j;->m:I

    and-int/2addr v0, p1

    if-eqz v0, :cond_0

    const/4 v0, 0x1

    :goto_0
    return v0

    :cond_0
    const/4 v0, 0x0

    goto :goto_0
.end method

.method public final f(B)Z
    .locals 1

    iget v0, p0, Lpmsj/work/b/j;->f:I

    invoke-static {p1, v0}, Lpmsj/work/b/j;->b(BI)Z

    move-result v0

    return v0
.end method

.method public final g(B)Z
    .locals 4

    const/4 v3, 0x1

    const/4 v2, 0x0

    iget v0, p0, Lpmsj/work/b/j;->f:I

    packed-switch p1, :pswitch_data_0

    :pswitch_0
    move v0, v2

    :goto_0
    return v0

    :pswitch_1
    const v1, 0x133461c0

    if-lt v0, v1, :cond_0

    const v1, 0x13347d18

    if-gt v0, v1, :cond_0

    move v0, v3

    goto :goto_0

    :cond_0
    move v0, v2

    goto :goto_0

    :pswitch_2
    const v1, 0x1334afe0

    if-lt v0, v1, :cond_1

    const v1, 0x13350da0

    if-le v0, v1, :cond_2

    :cond_1
    const v1, 0x13357330

    if-lt v0, v1, :cond_3

    const v1, 0x13359658

    if-gt v0, v1, :cond_3

    :cond_2
    move v0, v3

    goto :goto_0

    :cond_3
    move v0, v2

    goto :goto_0

    :pswitch_3
    const v1, 0x13317b91

    if-lt v0, v1, :cond_4

    const v1, 0x13317b9a

    if-gt v0, v1, :cond_4

    move v0, v3

    goto :goto_0

    :cond_4
    move v0, v2

    goto :goto_0

    nop

    :pswitch_data_0
    .packed-switch 0x1
        :pswitch_1
        :pswitch_2
        :pswitch_0
        :pswitch_3
    .end packed-switch
.end method

.method public h()I
    .locals 1

    const/4 v0, 0x0

    return v0
.end method

.method public final k(I)Z
    .locals 1

    iget-short v0, p0, Lpmsj/work/b/j;->j:S

    and-int/2addr v0, p1

    if-eqz v0, :cond_0

    const/4 v0, 0x1

    :goto_0
    return v0

    :cond_0
    const/4 v0, 0x0

    goto :goto_0
.end method

.method public final l(I)Ljava/lang/String;
    .locals 2

    iget-byte v0, p0, Lpmsj/work/b/j;->n:B

    if-gtz v0, :cond_0

    const/4 v0, 0x0

    :goto_0
    return-object v0

    :cond_0
    new-instance v0, Ljava/lang/StringBuffer;

    invoke-direct {v0}, Ljava/lang/StringBuffer;-><init>()V

    const-string v1, "\u7b49\u7ea7\u9700\u8981:"

    invoke-virtual {v0, v1}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    iget-byte v1, p0, Lpmsj/work/b/j;->n:B

    if-le v1, p1, :cond_1

    const-string v1, "*"

    invoke-virtual {v0, v1}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    sget-byte v1, Lpmsj/work/a/c;->n:B

    invoke-virtual {v0, v1}, Ljava/lang/StringBuffer;->append(I)Ljava/lang/StringBuffer;

    :cond_1
    iget-byte v1, p0, Lpmsj/work/b/j;->n:B

    invoke-virtual {v0, v1}, Ljava/lang/StringBuffer;->append(I)Ljava/lang/StringBuffer;

    invoke-virtual {v0}, Ljava/lang/StringBuffer;->toString()Ljava/lang/String;

    move-result-object v0

    goto :goto_0
.end method

.method public m()Ljava/util/Vector;
    .locals 5

    const/4 v2, 0x2

    const/4 v4, 0x1

    const/16 v3, 0x8

    new-instance v0, Ljava/util/Vector;

    invoke-direct {v0, v2}, Ljava/util/Vector;-><init>(I)V

    invoke-virtual {p0, v3}, Lpmsj/work/b/j;->d(I)Z

    move-result v1

    if-eqz v1, :cond_6

    invoke-virtual {p0, v3}, Lpmsj/work/b/j;->e(I)Z

    move-result v1

    if-nez v1, :cond_6

    const-string v1, "\u6fc0\u6d3b"

    invoke-virtual {v0, v1}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    :cond_0
    :goto_0
    const-string v1, "\u67e5\u770b"

    invoke-virtual {v0, v1}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    const/16 v1, 0x33

    iget-byte v2, p0, Lpmsj/work/b/j;->k:B

    if-eq v1, v2, :cond_2

    invoke-virtual {p0}, Lpmsj/work/b/j;->n()Z

    move-result v1

    if-eqz v1, :cond_2

    invoke-virtual {p0, v3}, Lpmsj/work/b/j;->e(I)Z

    move-result v1

    if-nez v1, :cond_2

    iget-short v1, p0, Lpmsj/work/b/j;->g:S

    if-le v1, v4, :cond_1

    const-string v1, "\u62c6\u5206"

    invoke-virtual {v0, v1}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    :cond_1
    iget-short v1, p0, Lpmsj/work/b/j;->g:S

    iget-short v2, p0, Lpmsj/work/b/j;->h:S

    if-ge v1, v2, :cond_2

    const-string v1, "\u5408\u5e76"

    invoke-virtual {v0, v1}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    :cond_2
    const/16 v1, 0x20

    invoke-virtual {p0, v1}, Lpmsj/work/b/j;->e(I)Z

    move-result v1

    if-eqz v1, :cond_3

    const-string v1, "\u89e3\u5c01"

    invoke-virtual {v0, v1}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    :cond_3
    iget-short v1, p0, Lpmsj/work/b/j;->l:S

    and-int/lit8 v1, v1, 0x10

    if-nez v1, :cond_4

    iget-short v1, p0, Lpmsj/work/b/j;->l:S

    and-int/lit16 v1, v1, 0x200

    if-eqz v1, :cond_7

    :cond_4
    move v1, v4

    :goto_1
    if-eqz v1, :cond_5

    const-string v1, "\u5408\u6210"

    invoke-virtual {v0, v1}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    :cond_5
    const-string v1, "\u4e22\u5f03"

    invoke-virtual {v0, v1}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    return-object v0

    :cond_6
    invoke-virtual {p0, v2}, Lpmsj/work/b/j;->k(I)Z

    move-result v1

    if-eqz v1, :cond_0

    const-string v1, "\u4f7f\u7528"

    invoke-virtual {v0, v1}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    goto :goto_0

    :cond_7
    const/4 v1, 0x0

    goto :goto_1
.end method

.method public final n()Z
    .locals 1

    iget-short v0, p0, Lpmsj/work/b/j;->l:S

    and-int/lit8 v0, v0, 0x40

    if-eqz v0, :cond_0

    const/4 v0, 0x1

    :goto_0
    return v0

    :cond_0
    const/4 v0, 0x0

    goto :goto_0
.end method

.method public o()Z
    .locals 1

    const/4 v0, 0x0

    return v0
.end method

.method public final p()Z
    .locals 2

    const/4 v1, 0x1

    invoke-virtual {p0, v1}, Lpmsj/work/b/j;->e(I)Z

    move-result v0

    if-nez v0, :cond_0

    const/4 v0, 0x4

    invoke-virtual {p0, v0}, Lpmsj/work/b/j;->e(I)Z

    move-result v0

    if-nez v0, :cond_0

    const/16 v0, 0x8

    invoke-virtual {p0, v0}, Lpmsj/work/b/j;->e(I)Z

    move-result v0

    if-eqz v0, :cond_1

    :cond_0
    move v0, v1

    :goto_0
    return v0

    :cond_1
    const/4 v0, 0x0

    goto :goto_0
.end method

.method public final q()Ljava/lang/String;
    .locals 6

    const v5, 0x8b0840

    const/16 v4, 0x20

    const/4 v3, 0x0

    new-instance v0, Ljava/lang/StringBuffer;

    invoke-direct {v0}, Ljava/lang/StringBuffer;-><init>()V

    iget-short v1, p0, Lpmsj/work/b/j;->q:S

    invoke-virtual {p0}, Lpmsj/work/b/j;->h()I

    move-result v2

    invoke-static {v3, v1, v2, v3}, Lpmsj/work/a/k;->a(IIII)Ljava/lang/String;

    move-result-object v1

    invoke-virtual {v0, v1}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    invoke-virtual {v0, v4}, Ljava/lang/StringBuffer;->append(C)Ljava/lang/StringBuffer;

    invoke-virtual {p0}, Lpmsj/work/b/j;->d()Ljava/lang/String;

    move-result-object v1

    invoke-virtual {v0, v1}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    invoke-virtual {p0}, Lpmsj/work/b/j;->p()Z

    move-result v1

    if-eqz v1, :cond_0

    const v1, 0x8b61d    # 8.00014E-40f

    invoke-static {v1, v3}, Lpmsj/work/a/k;->b(II)Ljava/lang/String;

    move-result-object v1

    invoke-virtual {v0, v1}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    :cond_0
    invoke-virtual {p0, v4}, Lpmsj/work/b/j;->e(I)Z

    move-result v1

    if-eqz v1, :cond_1

    const v1, 0x8d9a0

    invoke-static {v1, v3}, Lpmsj/work/a/k;->b(II)Ljava/lang/String;

    move-result-object v1

    invoke-virtual {v0, v1}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    :cond_1
    const/16 v1, 0x8

    invoke-virtual {p0, v1}, Lpmsj/work/b/j;->e(I)Z

    move-result v1

    if-eqz v1, :cond_2

    iget v1, p0, Lpmsj/work/b/j;->p:I

    if-lez v1, :cond_3

    invoke-static {v5, v3}, Lpmsj/work/a/k;->b(II)Ljava/lang/String;

    move-result-object v1

    invoke-virtual {v0, v1}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    :cond_2
    :goto_0
    invoke-virtual {v0}, Ljava/lang/StringBuffer;->toString()Ljava/lang/String;

    move-result-object v0

    return-object v0

    :cond_3
    iget v1, p0, Lpmsj/work/b/j;->p:I

    if-nez v1, :cond_2

    const/4 v1, 0x1

    invoke-static {v5, v1}, Lpmsj/work/a/k;->b(II)Ljava/lang/String;

    move-result-object v1

    invoke-virtual {v0, v1}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    goto :goto_0
.end method

.method public final r()Ljava/lang/String;
    .locals 3

    invoke-virtual {p0}, Lpmsj/work/b/j;->n()Z

    move-result v0

    if-eqz v0, :cond_0

    iget-short v0, p0, Lpmsj/work/b/j;->g:S

    const/4 v1, 0x1

    if-gt v0, v1, :cond_1

    :cond_0
    const-string v0, ""

    :goto_0
    return-object v0

    :cond_1
    new-instance v0, Ljava/lang/StringBuffer;

    invoke-direct {v0}, Ljava/lang/StringBuffer;-><init>()V

    const/16 v1, 0x20

    invoke-virtual {v0, v1}, Ljava/lang/StringBuffer;->append(C)Ljava/lang/StringBuffer;

    const-string v1, "*"

    invoke-virtual {v0, v1}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    iget-short v1, p0, Lpmsj/work/b/j;->h:S

    iget-short v2, p0, Lpmsj/work/b/j;->g:S

    if-ne v1, v2, :cond_2

    sget-byte v1, Lpmsj/work/a/c;->o:B

    invoke-virtual {v0, v1}, Ljava/lang/StringBuffer;->append(I)Ljava/lang/StringBuffer;

    :goto_1
    const/16 v1, 0xd7

    invoke-virtual {v0, v1}, Ljava/lang/StringBuffer;->append(C)Ljava/lang/StringBuffer;

    iget-short v1, p0, Lpmsj/work/b/j;->g:S

    invoke-virtual {v0, v1}, Ljava/lang/StringBuffer;->append(I)Ljava/lang/StringBuffer;

    invoke-virtual {v0}, Ljava/lang/StringBuffer;->toString()Ljava/lang/String;

    move-result-object v0

    goto :goto_0

    :cond_2
    sget-byte v1, Lpmsj/work/a/c;->l:B

    invoke-virtual {v0, v1}, Ljava/lang/StringBuffer;->append(I)Ljava/lang/StringBuffer;

    goto :goto_1
.end method

.method public final s()Ljava/lang/String;
    .locals 4

    const/16 v3, 0x3e8

    const/4 v2, 0x1

    iget v0, p0, Lpmsj/work/b/j;->i:I

    const/16 v1, 0xa

    if-ge v0, v1, :cond_1

    iget v0, p0, Lpmsj/work/b/j;->i:I

    shr-int/lit8 v0, v0, 0x1

    invoke-static {v2, v0}, Ljava/lang/Math;->max(II)I

    move-result v0

    :goto_0
    invoke-virtual {p0}, Lpmsj/work/b/j;->n()Z

    move-result v1

    if-eqz v1, :cond_0

    iget-short v1, p0, Lpmsj/work/b/j;->g:S

    mul-int/2addr v0, v1

    :cond_0
    invoke-static {v0}, La/c/x;->g(I)Ljava/lang/String;

    move-result-object v0

    return-object v0

    :cond_1
    iget v0, p0, Lpmsj/work/b/j;->i:I

    const/16 v1, 0x64

    if-ge v0, v1, :cond_2

    iget v0, p0, Lpmsj/work/b/j;->i:I

    mul-int/lit8 v0, v0, 0x3

    div-int/lit8 v0, v0, 0xa

    invoke-static {v2, v0}, Ljava/lang/Math;->max(II)I

    move-result v0

    goto :goto_0

    :cond_2
    iget v0, p0, Lpmsj/work/b/j;->i:I

    if-ge v0, v3, :cond_3

    const/16 v0, 0x1e

    iget v1, p0, Lpmsj/work/b/j;->i:I

    div-int/lit8 v1, v1, 0x5

    invoke-static {v0, v1}, Ljava/lang/Math;->max(II)I

    move-result v0

    goto :goto_0

    :cond_3
    iget v0, p0, Lpmsj/work/b/j;->i:I

    const/16 v1, 0x2710

    if-ge v0, v1, :cond_4

    const/16 v0, 0xc8

    iget v1, p0, Lpmsj/work/b/j;->i:I

    div-int/lit8 v1, v1, 0xa

    invoke-static {v0, v1}, Ljava/lang/Math;->max(II)I

    move-result v0

    goto :goto_0

    :cond_4
    iget v0, p0, Lpmsj/work/b/j;->i:I

    div-int/lit8 v0, v0, 0x14

    invoke-static {v3, v0}, Ljava/lang/Math;->max(II)I

    move-result v0

    goto :goto_0
.end method
