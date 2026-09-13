.class public final Lpmsj/work/e/ev;
.super Lpmsj/work/e/cd;


# instance fields
.field private final K:I

.field private L:Lpmsj/work/d/g;

.field private M:[I

.field private final N:B

.field private final O:B

.field private final f:I


# direct methods
.method public constructor <init>()V
    .locals 1

    invoke-direct {p0}, Lpmsj/work/e/cd;-><init>()V

    const v0, 0x95a89

    iput v0, p0, Lpmsj/work/e/ev;->f:I

    const/16 v0, 0x2720

    iput v0, p0, Lpmsj/work/e/ev;->K:I

    const/4 v0, 0x1

    iput-byte v0, p0, Lpmsj/work/e/ev;->N:B

    const/4 v0, 0x2

    iput-byte v0, p0, Lpmsj/work/e/ev;->O:B

    return-void
.end method


# virtual methods
.method public final a(Lpmsj/work/main/w;)V
    .locals 7

    const/4 v6, 0x0

    invoke-super {p0, p1}, Lpmsj/work/e/cd;->a(Lpmsj/work/main/w;)V

    invoke-virtual {p1, v6}, Lpmsj/work/main/w;->a(I)B

    move-result v0

    packed-switch v0, :pswitch_data_0

    :cond_0
    :goto_0
    return-void

    :pswitch_0
    const/4 v0, 0x1

    invoke-virtual {p1, v0}, Lpmsj/work/main/w;->a(I)B

    move-result v0

    if-eqz v0, :cond_0

    iget-object v1, p1, Lpmsj/work/main/w;->b:Ljava/util/Vector;

    invoke-virtual {v1}, Ljava/util/Vector;->size()I

    move-result v1

    const/4 v2, 0x2

    sub-int/2addr v1, v2

    div-int/2addr v1, v0

    iget-object v2, p0, Lpmsj/work/e/ev;->a:Ljava/util/Vector;

    invoke-virtual {v2}, Ljava/util/Vector;->size()I

    move-result v2

    if-eqz v2, :cond_1

    iget-object v2, p0, Lpmsj/work/e/ev;->a:Ljava/util/Vector;

    invoke-virtual {v2}, Ljava/util/Vector;->removeAllElements()V

    :cond_1
    move v2, v6

    :goto_1
    if-ge v2, v0, :cond_3

    mul-int v3, v2, v1

    add-int/lit8 v3, v3, 0x2

    invoke-static {v1, v3, p1}, La/c/x;->a(IILpmsj/work/main/w;)[La/c/i;

    move-result-object v3

    aget-object v4, v3, v6

    invoke-virtual {v4}, La/c/i;->b()I

    move-result v4

    iget-object v5, p0, Lpmsj/work/e/ev;->a:Ljava/util/Vector;

    invoke-static {v4, v5}, Lpmsj/work/e/ev;->a(ILjava/util/Vector;)Z

    move-result v4

    if-nez v4, :cond_2

    iget-object v4, p0, Lpmsj/work/e/ev;->a:Ljava/util/Vector;

    invoke-virtual {v4, v3}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    :cond_2
    add-int/lit8 v2, v2, 0x1

    goto :goto_1

    :cond_3
    iget-object v0, p0, Lpmsj/work/e/ev;->a:Ljava/util/Vector;

    invoke-virtual {p0, v0}, Lpmsj/work/e/ev;->b(Ljava/util/Vector;)V

    goto :goto_0

    :pswitch_data_0
    .packed-switch 0x3
        :pswitch_0
    .end packed-switch
.end method

.method protected final b(Ljava/util/Vector;)V
    .locals 7

    const/4 v4, 0x1

    const/4 v6, 0x0

    invoke-virtual {p1}, Ljava/util/Vector;->size()I

    move-result v0

    invoke-virtual {p0}, Lpmsj/work/e/ev;->af()I

    move-result v1

    const/16 v2, 0xaf9

    if-ne v1, v2, :cond_1

    const/4 v1, 0x3

    :goto_0
    new-array v2, v1, [I

    iget-object v3, p0, Lpmsj/work/e/ev;->L:Lpmsj/work/d/g;

    invoke-virtual {v3}, Lpmsj/work/d/g;->h()I

    move-result v3

    if-le v3, v4, :cond_0

    iget-object v3, p0, Lpmsj/work/e/ev;->L:Lpmsj/work/d/g;

    invoke-virtual {v3, v4}, Lpmsj/work/d/g;->c(I)V

    :cond_0
    new-array v3, v4, [I

    iget-object v4, p0, Lpmsj/work/e/ev;->L:Lpmsj/work/d/g;

    iget v4, v4, Lpmsj/work/d/b;->l:I

    aput v4, v3, v6

    move v4, v6

    :goto_1
    if-ge v4, v1, :cond_2

    iget-object v5, p0, Lpmsj/work/e/ev;->L:Lpmsj/work/d/g;

    iget v5, v5, Lpmsj/work/d/b;->k:I

    div-int/2addr v5, v1

    aput v5, v2, v4

    add-int/lit8 v4, v4, 0x1

    goto :goto_1

    :cond_1
    invoke-virtual {p0}, Lpmsj/work/e/ev;->af()I

    move-result v1

    const/16 v2, 0x9c4

    if-ne v1, v2, :cond_4

    const/4 v1, 0x2

    goto :goto_0

    :cond_2
    iget-object v1, p0, Lpmsj/work/e/ev;->L:Lpmsj/work/d/g;

    const/4 v4, 0x0

    invoke-virtual {v1, v2, v3, v4}, Lpmsj/work/d/g;->a([I[I[I)V

    iget-object v1, p0, Lpmsj/work/e/ev;->L:Lpmsj/work/d/g;

    invoke-virtual {v1, v0}, Lpmsj/work/d/g;->c(I)V

    move v1, v6

    :goto_2
    if-ge v1, v0, :cond_3

    new-instance v2, Lpmsj/work/d/a;

    invoke-static {p1, v1}, Lpmsj/work/e/ev;->a(Ljava/util/Vector;I)Ljava/lang/String;

    move-result-object v3

    sget-object v4, Lpmsj/work/a/c;->v:[I

    const/16 v5, 0x9

    aget v4, v4, v5

    invoke-direct {v2, v3, v4}, Lpmsj/work/d/a;-><init>(Ljava/lang/String;I)V

    iget-object v3, p0, Lpmsj/work/e/ev;->L:Lpmsj/work/d/g;

    invoke-virtual {v3, v2, v1}, Lpmsj/work/d/g;->a(Lpmsj/work/d/b;I)V

    add-int/lit8 v1, v1, 0x1

    goto :goto_2

    :cond_3
    return-void

    :cond_4
    move v1, v6

    goto :goto_0
.end method

.method protected final b(Lpmsj/work/d/b;)V
    .locals 6

    const/16 v2, 0xaf9

    const/16 v5, 0x49

    const/4 v4, 0x1

    const/4 v3, 0x0

    iget-object v0, p0, Lpmsj/work/e/ev;->d:Lpmsj/work/d/k;

    if-ne p1, v0, :cond_0

    iget-object v0, p0, Lpmsj/work/e/ev;->M:[I

    invoke-virtual {p0, v0}, Lpmsj/work/e/ev;->a([I)V

    invoke-virtual {p0}, Lpmsj/work/e/ev;->af()I

    move-result v0

    invoke-virtual {p0, v0}, Lpmsj/work/e/ev;->y(I)V

    iget-object v0, p0, Lpmsj/work/e/ev;->e:Lpmsj/work/d/c;

    invoke-virtual {v0}, Lpmsj/work/d/c;->aj()V

    iget-object v0, p0, Lpmsj/work/e/ev;->L:Lpmsj/work/d/g;

    invoke-virtual {v0, v3}, Lpmsj/work/d/g;->h(I)V

    :cond_0
    iget-object v0, p0, Lpmsj/work/e/ev;->L:Lpmsj/work/d/g;

    if-ne p1, v0, :cond_1

    iget-object v0, p0, Lpmsj/work/e/ev;->L:Lpmsj/work/d/g;

    invoke-virtual {v0}, Lpmsj/work/d/g;->f()I

    move-result v1

    iget-object v0, p0, Lpmsj/work/e/ev;->a:Ljava/util/Vector;

    invoke-virtual {v0}, Ljava/util/Vector;->size()I

    move-result v0

    if-lt v1, v0, :cond_2

    :cond_1
    :goto_0
    return-void

    :cond_2
    invoke-virtual {p0}, Lpmsj/work/e/ev;->af()I

    move-result v0

    if-ne v0, v2, :cond_7

    iget v0, p0, Lpmsj/work/e/ev;->I:I

    if-ne v2, v0, :cond_6

    iget-object v0, p0, Lpmsj/work/e/ev;->a:Ljava/util/Vector;

    invoke-virtual {v0}, Ljava/util/Vector;->size()I

    if-ltz v1, :cond_3

    iget-object v0, p0, Lpmsj/work/e/ev;->a:Ljava/util/Vector;

    if-eqz v0, :cond_3

    iget-object v0, p0, Lpmsj/work/e/ev;->a:Ljava/util/Vector;

    invoke-virtual {v0}, Ljava/util/Vector;->size()I

    move-result v0

    if-eqz v0, :cond_3

    iget-object v0, p0, Lpmsj/work/e/ev;->a:Ljava/util/Vector;

    invoke-virtual {v0}, Ljava/util/Vector;->size()I

    move-result v0

    if-ge v0, v1, :cond_4

    :cond_3
    const/4 v0, -0x1

    :goto_1
    if-ne v0, v4, :cond_5

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v2, 0x2c

    invoke-virtual {v0, v2}, Lpmsj/work/d/n;->f(I)Lpmsj/work/d/c;

    move-result-object v0

    iget-object v2, p0, Lpmsj/work/e/ev;->a:Ljava/util/Vector;

    invoke-static {v2, v1}, Lpmsj/work/e/ev;->a(Ljava/util/Vector;I)Ljava/lang/String;

    move-result-object v2

    invoke-virtual {v0, v2}, Lpmsj/work/d/c;->d(Ljava/lang/String;)V

    const/16 v0, 0x472

    const/16 v2, 0xd

    invoke-virtual {p0, v1}, Lpmsj/work/e/ev;->C(I)I

    move-result v1

    int-to-byte v1, v1

    invoke-static {v0, v2, v1}, Lpmsj/work/main/w;->a(IBB)V

    goto :goto_0

    :cond_4
    iget-object v0, p0, Lpmsj/work/e/ev;->a:Ljava/util/Vector;

    invoke-virtual {v0, v1}, Ljava/util/Vector;->elementAt(I)Ljava/lang/Object;

    move-result-object v0

    check-cast v0, [La/c/i;

    const/4 v2, 0x2

    aget-object v0, v0, v2

    invoke-virtual {v0}, La/c/i;->b()I

    move-result v0

    goto :goto_1

    :cond_5
    invoke-virtual {p0, v1}, Lpmsj/work/e/ev;->C(I)I

    move-result v0

    iget-object v2, p0, Lpmsj/work/e/ev;->a:Ljava/util/Vector;

    invoke-static {v2, v1}, Lpmsj/work/e/ev;->a(Ljava/util/Vector;I)Ljava/lang/String;

    mul-int/lit8 v0, v0, 0xa

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v1

    invoke-virtual {v1, v5}, Lpmsj/work/d/n;->f(I)Lpmsj/work/d/c;

    move-result-object p0

    check-cast p0, Lpmsj/work/e/p;

    invoke-virtual {p0, v4, v3, v3}, Lpmsj/work/e/p;->a(BII)V

    invoke-virtual {p0, v0}, Lpmsj/work/e/p;->y(I)V

    goto :goto_0

    :cond_6
    const/16 v0, 0xafa

    iget v2, p0, Lpmsj/work/e/ev;->I:I

    if-ne v0, v2, :cond_1

    invoke-virtual {p0, v1}, Lpmsj/work/e/ev;->C(I)I

    move-result v0

    iget-object v2, p0, Lpmsj/work/e/ev;->a:Ljava/util/Vector;

    invoke-static {v2, v1}, Lpmsj/work/e/ev;->a(Ljava/util/Vector;I)Ljava/lang/String;

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v1

    invoke-virtual {v1, v5}, Lpmsj/work/d/n;->f(I)Lpmsj/work/d/c;

    move-result-object p0

    check-cast p0, Lpmsj/work/e/p;

    const/16 v1, 0x17

    invoke-virtual {p0, v1, v3, v3}, Lpmsj/work/e/p;->a(BII)V

    invoke-virtual {p0, v0}, Lpmsj/work/e/p;->y(I)V

    goto/16 :goto_0

    :cond_7
    invoke-virtual {p0}, Lpmsj/work/e/ev;->af()I

    move-result v0

    const/16 v2, 0x9c4

    if-ne v0, v2, :cond_1

    const/16 v0, 0x42b

    iget v2, p0, Lpmsj/work/d/b;->g:I

    invoke-virtual {p0, v1}, Lpmsj/work/e/ev;->C(I)I

    move-result v1

    invoke-static {v0, v4, v2, v1}, Lpmsj/work/main/w;->a(IBII)V

    invoke-static {v4, v3}, Lpmsj/work/main/t;->a(ZZ)V

    goto/16 :goto_0
.end method

.method protected final c()V
    .locals 8

    const/16 v7, 0x14

    const/4 v6, 0x2

    const/4 v5, 0x0

    const-string v0, "\u5bc4\u552e\u5546\u4eba"

    invoke-virtual {p0, v0}, Lpmsj/work/e/ev;->d(Ljava/lang/String;)V

    new-array v0, v6, [Ljava/lang/String;

    const-string v1, "\u8d2d\u4e70\u7269\u54c1"

    aput-object v1, v0, v5

    const/4 v1, 0x1

    const-string v2, "\u8d2d\u4e70\u5ba0\u7269"

    aput-object v2, v0, v1

    const v1, 0x95a89

    invoke-virtual {p0, v1, v0}, Lpmsj/work/e/ev;->a(I[Ljava/lang/String;)V

    const/16 v0, 0x266

    invoke-virtual {p0, v0}, Lpmsj/work/e/ev;->A(I)Lpmsj/work/d/c;

    move-result-object v0

    iput-object v0, p0, Lpmsj/work/e/ev;->e:Lpmsj/work/d/c;

    iget-object v0, p0, Lpmsj/work/e/ev;->e:Lpmsj/work/d/c;

    const/16 v1, 0x2000

    invoke-virtual {v0, v1}, Lpmsj/work/d/c;->q(I)V

    iget-object v0, p0, Lpmsj/work/e/ev;->e:Lpmsj/work/d/c;

    iget-object v1, p0, Lpmsj/work/e/ev;->d:Lpmsj/work/d/k;

    iget-short v1, v1, Lpmsj/work/d/b;->i:S

    iget-object v2, p0, Lpmsj/work/e/ev;->d:Lpmsj/work/d/k;

    invoke-virtual {v2}, Lpmsj/work/d/k;->E()I

    move-result v2

    add-int/lit8 v2, v2, 0x2

    iget-short v3, p0, Lpmsj/work/e/ev;->j:S

    sub-int/2addr v2, v3

    sget-short v3, Lpmsj/work/main/t;->d:S

    iget v4, p0, Lpmsj/work/e/ev;->l:I

    sub-int/2addr v3, v4

    shr-int/lit8 v3, v3, 0x1

    add-int/2addr v2, v3

    invoke-virtual {v0, v1, v2}, Lpmsj/work/d/c;->f(II)V

    iget-object v0, p0, Lpmsj/work/e/ev;->e:Lpmsj/work/d/c;

    iget v1, p0, Lpmsj/work/e/ev;->k:I

    sub-int/2addr v1, v7

    iget v2, p0, Lpmsj/work/e/ev;->l:I

    iget-object v3, p0, Lpmsj/work/e/ev;->d:Lpmsj/work/d/k;

    iget v3, v3, Lpmsj/work/d/b;->l:I

    sub-int/2addr v2, v3

    iget v3, p0, Lpmsj/work/e/ev;->C:I

    sub-int/2addr v2, v3

    const/16 v3, 0x24

    sub-int/2addr v2, v3

    const/16 v3, 0x8

    sub-int/2addr v2, v3

    invoke-virtual {v0, v1, v2}, Lpmsj/work/d/c;->e(II)V

    new-array v0, v6, [I

    fill-array-data v0, :array_0

    iput-object v0, p0, Lpmsj/work/e/ev;->M:[I

    iget-object v0, p0, Lpmsj/work/e/ev;->e:Lpmsj/work/d/c;

    const/16 v1, 0x2720

    invoke-virtual {v0, v1}, Lpmsj/work/d/c;->w(I)Lpmsj/work/d/b;

    move-result-object v0

    check-cast v0, Lpmsj/work/d/g;

    iput-object v0, p0, Lpmsj/work/e/ev;->L:Lpmsj/work/d/g;

    iget-object v0, p0, Lpmsj/work/e/ev;->L:Lpmsj/work/d/g;

    iget-object v1, p0, Lpmsj/work/e/ev;->e:Lpmsj/work/d/c;

    iget-short v1, v1, Lpmsj/work/d/b;->i:S

    add-int/lit8 v1, v1, 0xa

    iget-object v2, p0, Lpmsj/work/e/ev;->e:Lpmsj/work/d/c;

    iget-short v2, v2, Lpmsj/work/d/c;->j:S

    add-int/lit8 v2, v2, 0xa

    sget-short v3, Lpmsj/work/main/t;->d:S

    iget v4, p0, Lpmsj/work/e/ev;->l:I

    sub-int/2addr v3, v4

    shr-int/lit8 v3, v3, 0x1

    sub-int/2addr v2, v3

    iget-short v3, p0, Lpmsj/work/e/ev;->j:S

    add-int/2addr v2, v3

    invoke-virtual {v0, v1, v2}, Lpmsj/work/d/g;->f(II)V

    iget-object v0, p0, Lpmsj/work/e/ev;->L:Lpmsj/work/d/g;

    iget-object v1, p0, Lpmsj/work/e/ev;->e:Lpmsj/work/d/c;

    iget v1, v1, Lpmsj/work/d/b;->k:I

    sub-int/2addr v1, v7

    iput v1, v0, Lpmsj/work/d/b;->k:I

    iget-object v0, p0, Lpmsj/work/e/ev;->L:Lpmsj/work/d/g;

    const/16 v1, 0x3400

    invoke-virtual {v0, v1}, Lpmsj/work/d/g;->l(I)V

    const/16 v0, 0x265

    iput v0, p0, Lpmsj/work/d/b;->g:I

    iget-object v0, p0, Lpmsj/work/e/ev;->M:[I

    invoke-virtual {p0, v0}, Lpmsj/work/e/ev;->a([I)V

    iget-object v0, p0, Lpmsj/work/e/ev;->e:Lpmsj/work/d/c;

    invoke-virtual {v0}, Lpmsj/work/d/c;->aj()V

    iget-object v0, p0, Lpmsj/work/e/ev;->L:Lpmsj/work/d/g;

    invoke-virtual {v0, v5}, Lpmsj/work/d/g;->h(I)V

    return-void

    :array_0
    .array-data 4
        0xaf9
        0x9c4
    .end array-data
.end method

.method protected final d(Lpmsj/work/d/b;)V
    .locals 2

    iget-object v0, p0, Lpmsj/work/e/ev;->d:Lpmsj/work/d/k;

    if-ne p1, v0, :cond_0

    iget-object v0, p0, Lpmsj/work/e/ev;->M:[I

    invoke-virtual {p0, v0}, Lpmsj/work/e/ev;->a([I)V

    invoke-virtual {p0}, Lpmsj/work/e/ev;->af()I

    move-result v0

    invoke-virtual {p0, v0}, Lpmsj/work/e/ev;->y(I)V

    iget-object v0, p0, Lpmsj/work/e/ev;->e:Lpmsj/work/d/c;

    invoke-virtual {v0}, Lpmsj/work/d/c;->aj()V

    iget-object v0, p0, Lpmsj/work/e/ev;->L:Lpmsj/work/d/g;

    const/4 v1, 0x0

    invoke-virtual {v0, v1}, Lpmsj/work/d/g;->h(I)V

    :cond_0
    return-void
.end method

.method public final i()I
    .locals 2

    iget-object v0, p0, Lpmsj/work/e/ev;->L:Lpmsj/work/d/g;

    invoke-virtual {v0}, Lpmsj/work/d/g;->f()I

    move-result v0

    if-ltz v0, :cond_0

    iget-object v1, p0, Lpmsj/work/e/ev;->a:Ljava/util/Vector;

    if-eqz v1, :cond_0

    iget-object v1, p0, Lpmsj/work/e/ev;->a:Ljava/util/Vector;

    invoke-virtual {v1}, Ljava/util/Vector;->size()I

    move-result v1

    if-eqz v1, :cond_0

    iget-object v1, p0, Lpmsj/work/e/ev;->a:Ljava/util/Vector;

    invoke-virtual {v1}, Ljava/util/Vector;->size()I

    move-result v1

    if-ge v1, v0, :cond_1

    :cond_0
    const/4 v0, -0x1

    :goto_0
    return v0

    :cond_1
    iget-object v1, p0, Lpmsj/work/e/ev;->a:Ljava/util/Vector;

    invoke-virtual {v1, v0}, Ljava/util/Vector;->elementAt(I)Ljava/lang/Object;

    move-result-object p0

    check-cast p0, [La/c/i;

    const/4 v0, 0x0

    aget-object v0, p0, v0

    invoke-virtual {v0}, La/c/i;->b()I

    move-result v0

    goto :goto_0
.end method

.method public final y(I)V
    .locals 2

    const/16 v0, 0x9c4

    if-ne p1, v0, :cond_1

    invoke-super {p0, p1}, Lpmsj/work/e/cd;->y(I)V

    const v0, 0x95a89

    invoke-virtual {p0, v0}, Lpmsj/work/e/ev;->w(I)Lpmsj/work/d/b;

    move-result-object p0

    check-cast p0, Lpmsj/work/d/k;

    const/4 v0, 0x1

    invoke-virtual {p0, v0}, Lpmsj/work/d/k;->c(I)V

    :cond_0
    :goto_0
    return-void

    :cond_1
    const/16 v0, 0xaf9

    if-ne p1, v0, :cond_0

    const/16 v0, 0x472

    const/4 v1, 0x3

    invoke-static {v0, v1}, Lpmsj/work/main/w;->a(IB)V

    goto :goto_0
.end method
